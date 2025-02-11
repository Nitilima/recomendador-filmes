from fastapi import APIRouter, HTTPException, Query
from data.database import filmes_collection
from models.filme import Filme, AtualizaFilme

filme_router = APIRouter()

# --------------------- Metodo Get ---------------------


@filme_router.get("/get-filmes")
async def get_filmes():
    filmes = list(filmes_collection.find({}, {"_id": 0}))
    if not filmes:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado")
    return filmes


@filme_router.get("/get-filme/{id_filme}")
async def get_filme(id_filme: int):
    filme = filmes_collection.find_one({"_id": id_filme})
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme


@filme_router.get("/get-filme-genero")
async def get_filme_genero(genero: str):
    filmes_genero = list(filmes_collection.find({"genero": genero}))
    if not filmes_genero:
        raise HTTPException(
            status_code=404, detail="Nenhum filme encontrado para este gênero")
    return filmes_genero


# --------------------- Metodo Post ---------------------

@filme_router.post("/cadastra-filme")
async def cadastra_filme(filme: Filme):

    if filmes_collection.find_one({"_id": filme.id}):
        raise HTTPException(status_code=400, detail="Filme já existente")

    filme_dict = filme.dict()
    filme_dict["_id"] = filme_dict.pop("id")
    filmes_collection.insert_one(filme_dict)

    return filme_dict

# --------------------- Metodo Put ---------------------


@filme_router.put("/atualiza-filme/{id_filme}")
async def atualiza_filme(id_filme: int, filme: AtualizaFilme):
    filme_atual = filmes_collection.find_one({"_id": id_filme})
    if not filme_atual:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    # Atualiza apenas os campos fornecidos
    update_data = {k: v for k, v in filme.dict().items() if v is not None}
    filmes_collection.update_one({"_id": id_filme}, {"$set": update_data})

    return filmes_collection.find_one({"_id": id_filme})
# --------------------- Metodo Delete ---------------------


@filme_router.delete("/deleta-filme/{id_filme}")
async def deleta_filme(id_filme: int):
    resultado = filmes_collection.delete_one({"_id": id_filme})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return {"message": "Filme deletado com sucesso"}

# --------------------- Busca para o DB --> React ---------------------


@filme_router.get("/buscar-filmes")
def buscar_filmes(query: str = Query(None, description="Termo de pesquisa")):
    try:
        query_num = int(query)
    except ValueError:
        query_num = None

    filtros = {
        "$or": [
            {"nome": {"$regex": query, "$options": "i"}},
            {"genero": {"$regex": query, "$options": "i"}}
        ]
    }

    if query_num is not None:
        filtros["$or"].append({"ano": query_num})

    filmes = list(filmes_collection.find(filtros, {"_id": 0}))

    if not filmes:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado")

    return filmes
