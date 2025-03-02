import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
from flask import current_app


from autorizacion.modulos.envio_imagen.infraestructura.schema.v1.eventos import EventoValidacionEnvio_ImagenCreada
from autorizacion.modulos.envio_imagen.infraestructura.schema.v1.comandos import ComandoCrearValidacionEnvio_Imagen
from autorizacion.seedwork.infraestructura import utils

from autorizacion.modulos.envio_imagen.aplicacion.mapeadores import MapeadorImagenEnvio_ImagenDTOJson
from autorizacion.modulos.envio_imagen.aplicacion.servicios import ServicioValidacionEnvio_Imagen

def suscribirse_a_eventos():
    cliente = None
    try:
        print("Subscribiendose a eventos envio_imagen")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-validacion_envio_imagen', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='autorizacion-sub-eventos-envio_imagen', schema=AvroSchema(EventoValidacionEnvio_ImagenCreada))

        print("suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
        consumidor.close()
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        print("Subscribiendose a comandos envio_imagen")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-validacion_envio_imagen', 
                consumer_type=_pulsar.ConsumerType.Shared, 
                subscription_name='autorizacion-sub-comandos-envio_imagen', 
                schema=AvroSchema(ComandoCrearValidacionEnvio_Imagen)
            )     
        print("suscribirse_a_comandos()")

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            
            envio_imagen_dict = mensaje.value().data.__dict__            
            map_validacion = MapeadorImagenEnvio_ImagenDTOJson()
            validacion_dto = map_validacion.externo_a_dto(envio_imagen_dict)
            print("FINALIZADO VALIDACION HIPPA")
            sr = ServicioValidacionEnvio_Imagen()
            dto_final = sr.crear_validacion_envio_imagen(validacion_dto)

            consumidor.acknowledge(mensaje)     
        consumidor.close()
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()