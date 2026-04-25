from __future__ import annotations

import json
import numpy as np
import pandas as pd
from datetime import datetime
from fastapi import HTTPException

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score,
)

from api.config_path_api import METRICS_DIRECTORY_PATH
from api.schemas.schemas import (
    EntradaAvaliacao, ResultadoMetricas,
    MetricasClassificacao, MetricasRegressao,
    TipoModelo,
)
from api.services.modelos_service import carregar_modelo
from api.services.dados_service import _carregar_df


def _mape(y_true, y_pred) -> float | None:
    y_true = np.array(y_true, dtype=float)
    if np.any(y_true == 0):
        return None
    return float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)


def _montar_resultado(nome_modelo, tipo_modelo, y_true, y_pred, X, modelo) -> ResultadoMetricas:
    if tipo_modelo == TipoModelo.classificacao:
        multiclasse = len(np.unique(y_true)) > 2
        avg         = "weighted" if multiclasse else "binary"

        roc_auc = None
        try:
            proba = modelo.predict_proba(X)
            roc_auc = float(
                roc_auc_score(y_true, proba, multi_class="ovr", average="weighted")
                if multiclasse else roc_auc_score(y_true, proba[:, 1])
            )
        except Exception:
            pass

        metricas = MetricasClassificacao(
            acuracia          = float(accuracy_score(y_true, y_pred)),
            precisao          = float(precision_score(y_true, y_pred, average=avg, zero_division=0)),
            recall            = float(recall_score(y_true, y_pred, average=avg, zero_division=0)),
            f1_score          = float(f1_score(y_true, y_pred, average=avg, zero_division=0)),
            roc_auc           = roc_auc,
            matriz_confusao   = confusion_matrix(y_true, y_pred).tolist(),
            relatorio_classes = classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        )
    else:
        mse = float(mean_squared_error(y_true, y_pred))
        metricas = MetricasRegressao(
            mae  = float(mean_absolute_error(y_true, y_pred)),
            mse  = mse,
            rmse = float(np.sqrt(mse)),
            r2   = float(r2_score(y_true, y_pred)),
            mape = _mape(y_true, y_pred),
        )

    return ResultadoMetricas(
        tipo_modelo    = tipo_modelo,
        modelo_arquivo = nome_modelo,
        metricas       = metricas.model_dump(),
    )


def avaliar_modelo(nome_modelo: str, entrada: EntradaAvaliacao) -> ResultadoMetricas:
    """Avalia com dados enviados via JSON."""
    modelo = carregar_modelo(nome_modelo)

    try:
        df = pd.DataFrame(entrada.dados)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Dados inválidos: {str(e)}")

    if entrada.coluna_alvo not in df.columns:
        raise HTTPException(
            status_code=422,
            detail=f"Coluna alvo '{entrada.coluna_alvo}' não encontrada. Disponíveis: {df.columns.tolist()}",
        )

    y_true = df[entrada.coluna_alvo]
    X      = df.drop(columns=[entrada.coluna_alvo])

    try:
        y_pred = modelo.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

    return _montar_resultado(nome_modelo, entrada.tipo_modelo, y_true, y_pred, X, modelo)


def avaliar_modelo_dataset(
    nome_modelo:  str,
    tipo_modelo:  TipoModelo,
    coluna_alvo:  str,
    filtro_ano:   int | None = None,
    filtro_bioma: str | None = None,
    filtro_uf:    str | None = None,
    n_linhas:     int        = 5000,
) -> ResultadoMetricas:
    """Avalia diretamente sobre o bdqueimadas_completo.parquet."""
    if n_linhas > 50_000:
        raise HTTPException(status_code=422, detail="n_linhas não pode ultrapassar 50.000.")

    modelo = carregar_modelo(nome_modelo)
    df     = _carregar_df().copy()

    if filtro_ano   and "Ano"     in df.columns:
        df = df[df["Ano"] == filtro_ano]
    if filtro_bioma and "Bioma"   in df.columns:
        df = df[df["Bioma"].str.contains(filtro_bioma, case=False, na=False)]
    if filtro_uf    and "Nome_UF" in df.columns:
        df = df[df["Nome_UF"].str.contains(filtro_uf, case=False, na=False)]

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado com os filtros informados.")

    if coluna_alvo not in df.columns:
        raise HTTPException(
            status_code=422,
            detail=f"Coluna alvo '{coluna_alvo}' não encontrada. Disponíveis: {df.columns.tolist()}",
        )

    df     = df.head(n_linhas)
    y_true = df[coluna_alvo]
    X      = df.drop(columns=[coluna_alvo])

    try:
        y_pred = modelo.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

    return _montar_resultado(nome_modelo, tipo_modelo, y_true, y_pred, X, modelo)


def salvar_metricas(resultado: ResultadoMetricas, nome_arquivo: str | None = None) -> dict:
    """Salva o JSON de métricas em METRICS_DIRECTORY_PATH com timestamp."""
    nome = nome_arquivo or resultado.modelo_arquivo.replace(".joblib", "")
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = METRICS_DIRECTORY_PATH / f"{nome}_{ts}.json"

    METRICS_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultado.model_dump(), f, ensure_ascii=False, indent=2)

    return {"mensagem": "Métricas salvas com sucesso.", "arquivo": str(path)}