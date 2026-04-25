from fastapi import APIRouter, Query
from api.schemas.schemas import InfoModelo, ListaModelos
import api.services.modelos_service as svc
import lightgbm

router = APIRouter(prefix="/modelos", tags=["Modelos"])


@router.get(
    "/listar",
    response_model=ListaModelos,
    summary="Lista todos os modelos",
    description=(
        "Varre MODELS_DIRECTORY_PATH (definido no config_path) e retorna "
        "todos os arquivos .joblib com seus metadados: tipo, features, classes e tamanho."
    ),
)
def listar_modelos():
    return svc.listar_modelos()


@router.get(
    "/info",
    response_model=InfoModelo,
    summary="Detalhes de um modelo",
    description=(
        "Retorna tipo (classificacao/regressao), feature names, número de classes "
        "e tamanho em MB de um modelo específico. "
        "Informe apenas o nome do arquivo (ex: 'lgbm_classificacao.joblib')."
    ),
)
def info_modelo(
    nome: str = Query(..., description="Nome do arquivo .joblib (ex: lgbm_classificacao.joblib)"),
):
    return svc.obter_info_modelo(nome)


@router.delete(
    "/cache",
    summary="Limpa cache de modelos",
    description="Remove os modelos carregados em memória para liberar RAM.",
)
def limpar_cache():
    return svc.limpar_cache()