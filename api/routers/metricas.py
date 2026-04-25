from fastapi import APIRouter, Query
from api.schemas.schemas import EntradaAvaliacao, ResultadoMetricas, TipoModelo
import api.services.metricas_service as svc

router = APIRouter(prefix="/metricas", tags=["Métricas"])


@router.post(
    "/avaliar",
    response_model=ResultadoMetricas,
    summary="Avalia eficiência com dados via JSON",
    description=(
        "Recebe dados com a coluna alvo, prediz e retorna métricas.\n\n"
        "**Classificação:** Acurácia, Precisão, Recall, F1, ROC-AUC, Matriz de Confusão.\n\n"
        "**Regressão:** MAE, MSE, RMSE, R², MAPE."
    ),
)
def avaliar_modelo(
    nome_modelo: str = Query(..., description="Nome do arquivo .joblib"),
    entrada: EntradaAvaliacao = ...,
):
    return svc.avaliar_modelo(nome_modelo, entrada)


@router.get(
    "/avaliar-dataset",
    response_model=ResultadoMetricas,
    summary="Avalia eficiência usando o bdqueimadas_completo.parquet",
    description=(
        "Avalia o modelo diretamente sobre o dataset do projeto. "
        "Permite filtrar por ano, bioma e UF. "
        "Máximo de 50.000 linhas por avaliação."
    ),
)
def avaliar_modelo_dataset(
    nome_modelo:  str        = Query(..., description="Nome do arquivo .joblib"),
    tipo_modelo:  TipoModelo = Query(..., description="'classificacao' ou 'regressao'"),
    coluna_alvo:  str        = Query(..., description="Coluna y_true (ex: 'FRP' para regressão)"),
    filtro_ano:   int | None = Query(None, description="Filtrar por Ano (ex: 2023)"),
    filtro_bioma: str | None = Query(None, description="Filtrar por Bioma (ex: 'Cerrado')"),
    filtro_uf:    str | None = Query(None, description="Filtrar por Nome_UF (ex: 'Mato Grosso')"),
    n_linhas:     int        = Query(5000, ge=1, le=50000, description="Máx. de linhas"),
):
    return svc.avaliar_modelo_dataset(
        nome_modelo  = nome_modelo,
        tipo_modelo  = tipo_modelo,
        coluna_alvo  = coluna_alvo,
        filtro_ano   = filtro_ano,
        filtro_bioma = filtro_bioma,
        filtro_uf    = filtro_uf,
        n_linhas     = n_linhas,
    )


@router.post(
    "/salvar",
    summary="Salva métricas em disco",
    description=(
        "Persiste o JSON de métricas em METRICS_DIRECTORY_PATH "
        "(definido no config_path) com timestamp no nome do arquivo."
    ),
)
def salvar_metricas(
    resultado: ResultadoMetricas,
    nome_arquivo: str | None = Query(
        None,
        description="Nome base do arquivo (sem extensão). Padrão: nome do modelo.",
    ),
):
    return svc.salvar_metricas(resultado, nome_arquivo)