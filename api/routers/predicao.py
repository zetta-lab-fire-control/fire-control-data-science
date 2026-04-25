from fastapi import APIRouter, Query
from api.schemas.schemas import EntradaPredicao, ResultadoPredicao, TipoModelo
import api.services.predicao_service as svc

router = APIRouter(prefix="/predicao", tags=["Predição"])


@router.post(
    "/",
    response_model=ResultadoPredicao,
    summary="Predição via JSON",
    description=(
        "Envia registros no corpo da requisição e recebe as predições. "
        "O modelo é identificado apenas pelo nome do arquivo .joblib — "
        "o caminho completo é resolvido via MODELS_DIRECTORY_PATH do config_path.\n\n"
        "**Classificação** → retorna a classe de intensidade + probabilidades por classe.\n\n"
        "**Regressão** → retorna os valores contínuos preditos."
    ),
)
def predizer(
    nome_modelo: str = Query(..., description="Nome do arquivo .joblib (ex: lgbm_classificacao.joblib)"),
    entrada: EntradaPredicao = ...,
):
    return svc.realizar_predicao(nome_modelo, entrada)


@router.post(
    "/dataset",
    response_model=ResultadoPredicao,
    summary="Predição sobre o bdqueimadas_completo.parquet",
    description=(
        "Executa predição em lote diretamente sobre o dataset do projeto. "
        "Permite filtrar por ano, bioma e UF antes de predizer. "
        "Máximo de 10.000 linhas por requisição."
    ),
)
def predizer_dataset(
    nome_modelo:  str        = Query(..., description="Nome do arquivo .joblib"),
    tipo_modelo:  TipoModelo = Query(..., description="'classificacao' ou 'regressao'"),
    coluna_alvo:  str | None = Query(None, description="Coluna a remover antes da predição (ex: 'FRP')"),
    filtro_ano:   int | None = Query(None, description="Filtrar por Ano (ex: 2023)"),
    filtro_bioma: str | None = Query(None, description="Filtrar por Bioma (ex: 'Amazônia')"),
    filtro_uf:    str | None = Query(None, description="Filtrar por Nome_UF (ex: 'Pará')"),
    n_linhas:     int        = Query(1000, ge=1, le=10000, description="Máx. de linhas"),
):
    return svc.realizar_predicao_dataset(
        nome_modelo  = nome_modelo,
        tipo_modelo  = tipo_modelo,
        coluna_alvo  = coluna_alvo,
        filtro_ano   = filtro_ano,
        filtro_bioma = filtro_bioma,
        filtro_uf    = filtro_uf,
        n_linhas     = n_linhas,
    )