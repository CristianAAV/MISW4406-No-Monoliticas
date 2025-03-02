from autorizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from autorizacion.seedwork.aplicacion.queries import ejecutar_query as query
from autorizacion.modulos.validacion_usuario.infraestructura.repositorios import RepositorioValidacion_Usuario
from dataclasses import dataclass
from ..comandos.base import ReservaQueryBaseHandler
from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_Usuario
import uuid

@dataclass
class ObtenerValidacion_Usuario(Query):
    id: str

class ObtenerValidacion_UsuarioHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerValidacion_Usuario) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion_Usuario.__class__)
        reserva =  self.fabrica_validacion_usuario.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorValidacion_Usuario())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerValidacion_Usuario)
def ejecutar_query_obtener_reserva(query: ObtenerValidacion_Usuario):
    handler = ObtenerValidacion_UsuarioHandler()
    return handler.handle(query)