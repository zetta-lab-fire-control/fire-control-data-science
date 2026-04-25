from __future__ import annotations

import pandas as pd
from fastapi import HTTPException

from api.schemas.schemas import EntradaPredicao, ResultadoPredicao, TipoModelo
from api.services.modelos_service import carregar_modelo
from api.services.dados_service import _carregar_df


def realizar_predicao(nome_modelo: str, entrada: EntradaPredicao) -> ResultadoPredicao:
    """Predição sobre dados enviados via JSON."""
    modelo = carregar_modelo(nome_modelo)

    try:
        df = pd.DataFrame(entrada.dados)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao montar DataFrame: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=422, detail="Nenhum registro enviado para predição.")

    try:
        predicoes = modelo.predict(df).tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {str(e)}")

    probabilidades: list | None = None
    classes:        list | None = None

    if entrada.tipo_modelo == TipoModelo.classificacao:
        try:
            probabilidades = modelo.predict_proba(df).tolist()
            estimador = list(modelo.named_steps.values())[-1] if hasattr(modelo, "named_steps") else modelo
            if hasattr(estimador, "classes_"):
                classes = [str(c) for c in estimador.classes_]
        except Exception:
            pass

    return ResultadoPredicao(
        tipo_modelo    = entrada.tipo_modelo,
        total_linhas   = len(df),
        predicoes      = predicoes,
        probabilidades = probabilidades,
        classes        = classes,
    )


def realizar_predicao_dataset(
    nome_modelo:  str,
    tipo_modelo:  TipoModelo,
    coluna_alvo:  str | None = None,
    filtro_ano:   int | None = None,
    filtro_bioma: str | None = None,
    filtro_uf:    str | None = None,
    n_linhas:     int        = 1000,
) -> ResultadoPredicao:
    """Predição em lote diretamente sobre o bdqueimadas_completo.parquet."""
    if n_linhas > 10_000:
        raise HTTPException(status_code=422, detail="n_linhas não pode ultrapassar 10.000.")

    df = _carregar_df().copy()

    if filtro_ano   and "Ano"     in df.columns:
        df = df[df["Ano"] == filtro_ano]
    if filtro_bioma and "Bioma"   in df.columns:
        df = df[df["Bioma"].str.contains(filtro_bioma, case=False, na=False)]
    if filtro_uf    and "Nome_UF" in df.columns:
        df = df[df["Nome_UF"].str.contains(filtro_uf, case=False, na=False)]

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado com os filtros informados.")

    df = df.head(n_linhas)

    if coluna_alvo and coluna_alvo in df.columns:
        df = df.drop(columns=[coluna_alvo])

    return realizar_predicao(nome_modelo, EntradaPredicao(tipo_modelo=tipo_modelo, dados=df.to_dict(orient="records")))