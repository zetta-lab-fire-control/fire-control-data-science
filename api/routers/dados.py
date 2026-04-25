from fastapi import APIRouter, Query
from api.schemas.schemas import InfoDataset, AmostraDataset, FiltrosDataset
import api.services.dados_service as svc

router = APIRouter(prefix="/dados", tags=["Dados"])


@router.get(
    "/info",
    response_model=InfoDataset,
    summary="Metadados do dataset",
    description=(
        "Retorna metadados completos do bdqueimadas_completo.parquet: "
        "linhas, colunas, tamanho, nulos, período coberto, biomas e UFs presentes."
    ),
)
def info_dataset():
    return svc.obter_info()


@router.get(
    "/amostra",
    response_model=AmostraDataset,
    summary="Amostra sem filtros",
    description="Retorna as primeiras N linhas do dataset sem nenhum filtro aplicado.",
)
def amostra_dataset(
    n_linhas: int = Query(10, ge=1, le=500, description="Número de linhas (máx. 500)"),
):
    return svc.obter_amostra(n_linhas)


@router.post(
    "/filtrar",
    response_model=AmostraDataset,
    summary="Dados com filtros",
    description=(
        "Filtra o dataset por ano, mês, bioma, UF e/ou faixa de RiscoFogo. "
        "Retorna até `n_linhas` registros (máx. 5000)."
    ),
)
def dados_filtrados(filtros: FiltrosDataset):
    return svc.obter_dados_filtrados(filtros)


@router.get(
    "/estatisticas",
    summary="Estatísticas descritivas",
    description="Retorna count, mean, std, min, quartis e max das colunas numéricas.",
)
def estatisticas():
    return svc.obter_estatisticas()


@router.get(
    "/valores-unicos/{coluna}",
    summary="Valores únicos de uma coluna",
    description=(
        "Retorna todos os valores únicos de uma coluna categórica. "
        "Útil para montar filtros de Bioma, Nome_UF, Satelite, etc."
    ),
)
def valores_unicos(coluna: str):
    return svc.obter_valores_unicos(coluna)


@router.delete(
    "/cache",
    summary="Libera cache do dataset",
    description="Remove o DataFrame em memória. Útil após atualização do arquivo .parquet.",
)
def limpar_cache():
    return svc.invalidar_cache()