from abc import ABC, abstractmethod  # Importa herramientas para crear clases y métodos abstractos
from datetime import datetime  # Importa datetime para marcar fechas y horas en eventos y logs
from pathlib import Path  # Importa Path para manejar rutas de carpetas y archivos de forma segura
import logging  # Importa logging para registrar eventos y errores en archivo de logs


# ==============================================================================
# 1. CONFIGURACIÓN DE LOGS (REGISTRO DE EVENTOS Y ERRORES EN ARCHIVO)
# ==============================================================================

def configurar_logger(ruta_log: str = "logs/sistema_software_fj.log") -> logging.Logger:
    """Configura y devuelve un logger que escribe eventos y errores en un archivo .log."""
    archivo_log = Path(ruta_log)  # Convierte la ruta en objeto Path
    archivo_log.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta 'logs' si no existe

    logger = logging.getLogger("SoftwareFJLogger")  # Obtiene o crea el logger con nombre específico
    logger.setLevel(logging.INFO)  # Define el nivel mínimo de registro como INFO

    if not logger.handlers:  # Evita duplicar manejadores si se llama la función más de una vez
        manejador_archivo = logging.FileHandler(archivo_log, encoding="utf-8")  # Crea manejador hacia el archivo .log
        formato = logging.Formatter(  # Define el formato de cada línea del log
            "%(asctime)s | %(levelname)s | %(message)s",  # Incluye timestamp, nivel y mensaje
            datefmt="%Y-%m-%d %H:%M:%S"  # Formato legible de fecha y hora
        )
        manejador_archivo.setFormatter(formato)  # Aplica el formato al manejador de archivo
        logger.addHandler(manejador_archivo)  # Registra el manejador en el logger

    return logger  # Retorna el logger listo para usar


logger = configurar_logger()  # Inicializa el logger global del sistema


# ==============================================================================
# 2. EXCEPCIONES PERSONALIZADAS DEL DOMINIO
# ==============================================================================

class ErrorSoftwareFJ(Exception):
    """Excepción base personalizada para errores del sistema de Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        super().__init__(mensaje)  # Pasa el mensaje a la clase base Exception
        self.codigo = codigo  # Guarda un código identificador del error


class ValidacionEntidadError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de una entidad o parámetro no cumplen las reglas."""

    def __init__(self, mensaje: str, codigo: str = "ERR_VALIDACION"):
        super().__init__(mensaje, codigo)  # Inicializa con código de validación


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar o reservar un servicio inactivo o no disponible."""

    def __init__(self, mensaje: str, codigo: str = "ERR_SERVICIO_NO_DISP"):
        super().__init__(mensaje, codigo)  # Inicializa con código de disponibilidad


class OperacionReservaError(ErrorSoftwareFJ):
    """Se lanza cuando ocurre una operación inválida sobre una reserva."""

    def __init__(self, mensaje: str, codigo: str = "ERR_RESERVA"):
        super().__init__(mensaje, codigo)  # Inicializa con código de reserva


class CalculoFinancieroError(ErrorSoftwareFJ):
    """Se lanza cuando hay valores inconsistentes o inválidos en cálculos de costos."""

    def __init__(self, mensaje: str, codigo: str = "ERR_CALCULO"):
        super().__init__(mensaje, codigo)  # Inicializa con código de cálculo


# ==============================================================================
# 3. CLASE ABSTRACTA BASE PARA ENTIDADES DEL SISTEMA
# ==============================================================================

class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales dentro de Software FJ."""

    def __init__(self, identificador: str, nombre: str):
        self._identificador = self._validar_texto_no_vacio(identificador, "identificador")  # Atributo protegido de ID
        self._nombre = self._validar_texto_no_vacio(nombre, "nombre")  # Atributo protegido de nombre
        self._creado_en = datetime.now()  # Registra la fecha y hora de creación del objeto

    @staticmethod
    def _validar_texto_no_vacio(valor: str, campo: str) -> str:
        """Valida que un campo de texto sea string y no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():  # Verifica tipo string y contenido real
            raise ValidacionEntidadError(f"El campo '{campo}' debe ser un texto no vacío.")  # Lanza error de validación
        return valor.strip()  # Retorna el texto limpio de espacios laterales

    @property
    def identificador(self) -> str:
        """Devuelve el identificador de la entidad."""
        return self._identificador  # Retorna ID protegido

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la entidad."""
        return self._nombre  # Retorna nombre protegido

    @abstractmethod
    def resumen(self) -> str:
        """Método abstracto que cada entidad concreta debe implementar."""
        pass  # Obliga a subclases a definir su resumen


# ==============================================================================
# 4. CLASE CLIENTE CON ENCAPSULACIÓN Y VALIDACIONES ESTRICTAS
# ==============================================================================

class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador, nombre)  # Inicializa atributos base de EntidadBase
        self.__correo = ""  # Atributo privado para correo electrónico
        self.__telefono = ""  # Atributo privado para teléfono
        self.correo = correo  # Usa el setter para validar correo desde el inicio
        self.telefono = telefono  # Usa el setter para validar teléfono desde el inicio

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo  # Retorna correo privado

    @correo.setter
    def correo(self, nuevo_correo: str) -> None:
        """Valida y asigna un correo electrónico válido."""
        if not isinstance(nuevo_correo, str) or "@" not in nuevo_correo or "." not in nuevo_correo.split("@")[-1]:
            raise ValidacionEntidadError(f"Correo electrónico inválido para el cliente '{self._nombre}': {nuevo_correo}")
        self.__correo = nuevo_correo.strip().lower()  # Guarda correo normalizado

    @property
    def telefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self.__telefono  # Retorna teléfono privado

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        """Valida y asigna un número telefónico con al menos 7 dígitos."""
        limpio = str(nuevo_telefono).strip()  # Convierte y limpia espacios
        if not limpio.isdigit() or len(limpio) < 7:  # Verifica que solo tenga dígitos y longitud mínima
            raise ValidacionEntidadError(f"Teléfono inválido para el cliente '{self._nombre}': {nuevo_telefono}")
        self.__telefono = limpio  # Guarda teléfono validado

    def resumen(self) -> str:
        """Implementación polimórfica del resumen de un cliente."""
        return f"[Cliente {self._identificador}] {self._nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"


# ==============================================================================
# 5. CLASE ABSTRACTA SERVICIO Y SERVICIOS ESPECIALIZADOS (POLIMORFISMO)
# ==============================================================================

class Servicio(EntidadBase, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador, nombre)  # Inicializa ID y nombre
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:  # Valida tarifa positiva
            raise ValidacionEntidadError(f"La tarifa base de '{nombre}' debe ser mayor que cero.")
        self._tarifa_base = float(tarifa_base)  # Almacena tarifa base como float
        self._disponible = bool(disponible)  # Indica si el servicio está disponible

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para reserva."""
        return self._disponible  # Retorna estado de disponibilidad

    def cambiar_disponibilidad(self, estado: bool) -> None:
        """Actualiza la disponibilidad del servicio."""
        self._disponible = bool(estado)  # Cambia el estado booleano

    @abstractmethod
    def validar_parametros(self, duracion_horas: float, cantidad_unidades: int = 1) -> None:
        """Valida parámetros específicos de duración o unidades del servicio."""
        pass  # Cada subclase define sus reglas

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: float, cantidad_unidades: int = 1) -> float:
        """Calcula el costo antes de descuentos o impuestos según el tipo de servicio."""
        pass  # Implementado de forma distinta en cada subclase

    def calcular_costo(
        self,
        duracion_horas: float,
        cantidad_unidades: int = 1,
        descuento_porcentaje: float = 0.0,
        impuesto_porcentaje: float = 0.0
    ) -> float:
        """
        Simula sobrecarga mediante parámetros opcionales para calcular el costo final
        aplicando validación, subtotal por servicio, descuento e impuesto.
        """
        try:
            self.validar_parametros(duracion_horas, cantidad_unidades)  # Valida entradas antes de calcular
            if not (0 <= descuento_porcentaje < 100):  # Valida rango de descuento
                raise CalculoFinancieroError("El descuento debe estar entre 0 y menos de 100 por ciento.")
            if impuesto_porcentaje < 0:  # Valida que el impuesto no sea negativo
                raise CalculoFinancieroError("El impuesto no puede ser negativo.")

            subtotal = self.calcular_costo_base(duracion_horas, cantidad_unidades)  # Calcula subtotal polimórfico
            con_descuento = subtotal * (1 - descuento_porcentaje / 100.0)  # Aplica descuento porcentual
            total = con_descuento * (1 + impuesto_porcentaje / 100.0)  # Aplica impuesto porcentual

            if total <= 0:  # Verifica consistencia del resultado final
                raise CalculoFinancieroError("El costo calculado resultó menor o igual a cero.")

            return round(total, 2)  # Redondea a dos decimales
        except ErrorSoftwareFJ:
            raise  # Re-lanza excepciones propias sin alterarlas
        except Exception as exc:
            raise CalculoFinancieroError(f"Error inesperado al calcular costo del servicio '{self._nombre}'.") from exc

    def resumen(self) -> str:
        """Describe el servicio y su disponibilidad."""
        estado = "Disponible" if self._disponible else "No disponible"  # Etiqueta legible de estado
        return f"[Servicio {self._identificador}] {self._nombre} | Tarifa base: ${self._tarifa_base:,.2f} | {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de trabajo o capacitación."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, capacidad_maxima: int, disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)  # Llama constructor padre
        if capacidad_maxima <= 0:  # Valida capacidad positiva
            raise ValidacionEntidadError("La capacidad máxima de la sala debe ser mayor que 0.")
        self.capacidad_maxima = capacidad_maxima  # Guarda capacidad máxima de personas

    def validar_parametros(self, duracion_horas: float, cantidad_unidades: int = 1) -> None:
        """Valida duración mínima de 1 hora y cantidad de asistentes dentro de capacidad."""
        if duracion_horas <= 0 or duracion_horas > 24:  # Rango razonable de horas por reserva
            raise ValidacionEntidadError("La duración de reserva de sala debe estar entre 1 y 24 horas.")
        if cantidad_unidades <= 0 or cantidad_unidades > self.capacidad_maxima:  # Verifica aforo
            raise ValidacionEntidadError(
                f"Cantidad de asistentes ({cantidad_unidades}) excede o no cumple capacidad ({self.capacidad_maxima})."
            )

    def calcular_costo_base(self, duracion_horas: float, cantidad_unidades: int = 1) -> float:
        """Calcula costo por horas con recargo leve si supera las 4 horas."""
        recargo_extendido = 1.15 if duracion_horas > 4 else 1.0  # Aplica recargo del 15% si supera 4 horas
        return self._tarifa_base * duracion_horas * recargo_extendido  # Retorna costo base de sala

    def resumen(self) -> str:
        """Sobrescribe resumen con detalles de sala."""
        return f"{super().resumen()} | Tipo: Sala (Cap. máx: {self.capacidad_maxima})"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, stock_disponible: int, disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)  # Inicializa servicio base
        if stock_disponible < 0:  # Evita stock negativo
            raise ValidacionEntidadError("El stock de equipos no puede ser negativo.")
        self.stock_disponible = stock_disponible  # Guarda unidades disponibles

    def validar_parametros(self, duracion_horas: float, cantidad_unidades: int = 1) -> None:
        """Valida horas de alquiler y disponibilidad de stock de equipos."""
        if duracion_horas <= 0:  # Duración positiva obligatoria
            raise ValidacionEntidadError("La duración del alquiler de equipo debe ser mayor a 0 horas.")
        if cantidad_unidades <= 0 or cantidad_unidades > self.stock_disponible:  # Verifica stock suficiente
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self._nombre}': solicitados {cantidad_unidades}, disponibles {self.stock_disponible}."
            )

    def calcular_costo_base(self, duracion_horas: float, cantidad_unidades: int = 1) -> float:
        """Calcula costo multiplicando tarifa por cantidad de equipos y horas."""
        return self._tarifa_base * cantidad_unidades * duracion_horas  # Costo proporcional a unidades y tiempo

    def resumen(self) -> str:
        """Sobrescribe resumen con información de stock."""
        return f"{super().resumen()} | Tipo: Alquiler Equipo (Stock: {self.stock_disponible})"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, modalidad: str = "Remota", disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)  # Inicializa servicio base
        self.modalidad = self._validar_texto_no_vacio(modalidad, "modalidad")  # Guarda modalidad validada

    def validar_parametros(self, duracion_horas: float, cantidad_unidades: int = 1) -> None:
        """Valida bloques de asesoría y número de sesiones."""
        if duracion_horas < 0.5 or duracion_horas > 12:  # Mínimo media hora, máximo 12 horas
            raise ValidacionEntidadError("La duración de asesoría debe estar entre 0.5 y 12 horas.")
        if cantidad_unidades <= 0:  # Al menos 1 sesión
            raise ValidacionEntidadError("La cantidad de sesiones de asesoría debe ser al menos 1.")

    def calcular_costo_base(self, duracion_horas: float, cantidad_unidades: int = 1) -> float:
        """Calcula costo de asesoría por sesión y duración."""
        return self._tarifa_base * cantidad_unidades * duracion_horas  # Costo total por sesiones y horas

    def resumen(self) -> str:
        """Sobrescribe resumen con modalidad de asesoría."""
        return f"{super().resumen()} | Tipo: Asesoría ({self.modalidad})"


# ==============================================================================
# 6. CLASE RESERVA Y GESTOR EN MEMORIA (SIN BASE DE DATOS)
# ==============================================================================

class Reserva:
    """Integra un cliente, un servicio, duración, unidades y ciclo de estados."""

    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}  # Conjunto de estados permitidos

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion_horas: float, unidades: int = 1):
        if not codigo or not isinstance(codigo, str):  # Valida código de reserva
            raise ValidacionEntidadError("El código de reserva es obligatorio.")
        if not isinstance(cliente, Cliente):  # Valida instancia de Cliente
            raise ValidacionEntidadError("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):  # Valida instancia de Servicio
            raise ValidacionEntidadError("La reserva requiere un objeto Servicio válido.")

        self.codigo = codigo.strip()  # Guarda código limpio
        self.cliente = cliente  # Asocia cliente
        self.servicio = servicio  # Asocia servicio
        self.duracion_horas = duracion_horas  # Guarda duración solicitada
        self.unidades = unidades  # Guarda unidades o personas solicitadas
        self.estado = "PENDIENTE"  # Estado inicial por defecto
        self.monto_total = 0.0  # Monto calculado al confirmar/procesar

    def confirmar(self, descuento_porcentaje: float = 0.0, impuesto_porcentaje: float = 0.0) -> float:
        """Confirma la reserva verificando disponibilidad, parámetros y calculando costo."""
        if self.estado == "CANCELADA":  # Impide confirmar una reserva cancelada
            raise OperacionReservaError(f"No se puede confirmar la reserva {self.codigo} porque está cancelada.")
        if not self.servicio.disponible:  # Verifica disponibilidad del servicio
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")

        self.monto_total = self.servicio.calcular_costo(  # Calcula costo usando método con parámetros opcionales
            duracion_horas=self.duracion_horas,
            cantidad_unidades=self.unidades,
            descuento_porcentaje=descuento_porcentaje,
            impuesto_porcentaje=impuesto_porcentaje
        )
        self.estado = "CONFIRMADA"  # Cambia estado a confirmada
        return self.monto_total  # Devuelve el monto total confirmado

    def cancelar(self, motivo: str = "Cancelada por solicitud del usuario") -> None:
        """Cancela la reserva si aún no fue procesada."""
        if self.estado == "PROCESADA":  # No permite cancelar reservas ya procesadas
            raise OperacionReservaError(f"La reserva {self.codigo} ya fue procesada y no puede cancelarse.")
        self.estado = "CANCELADA"  # Actualiza estado a cancelada
        logger.info(f"Reserva {self.codigo} cancelada. Motivo: {motivo}")  # Registra cancelación en log

    def procesar(self) -> str:
        """Procesa una reserva confirmada para darla por ejecutada."""
        if self.estado != "CONFIRMADA":  # Exige que esté confirmada previamente
            raise OperacionReservaError(
                f"La reserva {self.codigo} debe estar CONFIRMADA para procesarse (estado actual: {self.estado})."
            )
        self.estado = "PROCESADA"  # Cambia estado final a procesada
        return f"Reserva {self.codigo} procesada exitosamente por ${self.monto_total:,.2f}."


class GestorSoftwareFJ:
    """Administra listas en memoria de clientes, servicios y reservas sin base de datos."""

    def __init__(self):
        self.clientes: list[Cliente] = []  # Lista interna de clientes registrados
        self.servicios: list[Servicio] = []  # Lista interna de servicios disponibles
        self.reservas: list[Reserva] = []  # Lista interna de reservas

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista interna evitando IDs duplicados."""
        if any(c.identificador == cliente.identificador for c in self.clientes):  # Verifica duplicado por ID
            raise ValidacionEntidadError(f"Ya existe un cliente con ID '{cliente.identificador}'.")
        self.clientes.append(cliente)  # Agrega cliente a la lista
        logger.info(f"Cliente registrado: {cliente.resumen()}")  # Registra evento exitoso

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Agrega un servicio a la lista interna evitando IDs duplicados."""
        if any(s.identificador == servicio.identificador for s in self.servicios):  # Verifica duplicado por ID
            raise ValidacionEntidadError(f"Ya existe un servicio con ID '{servicio.identificador}'.")
        self.servicios.append(servicio)  # Agrega servicio a la lista
        logger.info(f"Servicio registrado: {servicio.resumen()}")  # Registra evento exitoso

    def crear_reserva(self, reserva: Reserva) -> None:
        """Agrega una reserva a la lista interna evitando códigos duplicados."""
        if any(r.codigo == reserva.codigo for r in self.reservas):  # Verifica duplicado por código
            raise OperacionReservaError(f"Ya existe una reserva con código '{reserva.codigo}'.")
        self.reservas.append(reserva)  # Agrega reserva a la lista
        logger.info(f"Reserva creada: {reserva.codigo} para {reserva.cliente.nombre}")  # Registra evento en log


# ==============================================================================
# 7. SIMULACIÓN DE 10+ OPERACIONES (VÁLIDAS E INVÁLIDAS) CON MANEJO ROBUSTO
# ==============================================================================

def ejecutar_simulacion() -> None:
    """Ejecuta 12 operaciones completas (válidas e inválidas) demostrando resiliencia."""
    gestor = GestorSoftwareFJ()  # Instancia el gestor principal en memoria
    operaciones_exitosas = 0  # Contador de operaciones completadas sin error

    def ejecutar_paso(descripcion: str, accion) -> None:
        """Envuelve cada operación en try/except/else/finally para garantizar continuidad."""
        nonlocal operaciones_exitosas  # Permite modificar el contador externo
        print(f"\n--- {descripcion} ---")  # Muestra descripción en consola
        try:
            resultado = accion()  # Intenta ejecutar la operación
        except ErrorSoftwareFJ as err:  # Captura excepciones propias del sistema
            logger.error(f"[{err.codigo}] Fallo en '{descripcion}': {err}")  # Registra error controlado en .log
            print(f"Error controlado ({err.codigo}): {err}")  # Informa sin detener el programa
        except Exception as exc:  # Captura cualquier otra excepción inesperada
            logger.exception(f"Error no previsto en '{descripcion}': {exc}")  # Registra traza completa en .log
            print(f"Error inesperado registrado en log: {exc}")  # Informa sin detener el programa
        else:
            operaciones_exitosas += 1  # Incrementa contador si no hubo excepciones
            logger.info(f"Éxito en '{descripcion}': {resultado}")  # Registra éxito en .log
            print(f"Éxito: {resultado}")  # Muestra resultado exitoso
        finally:
            print(f"Fin de intento -> {descripcion}")  # Se ejecuta siempre al cerrar el bloque

    # Operación 1 (Válida): Registro de cliente válido
    cliente_ana = Cliente("CLI-01", "Ana María Rojas", "ana.rojas@correo.com", "3104567890")
    ejecutar_paso("Op 1: Registrar cliente válido", lambda: (gestor.registrar_cliente(cliente_ana), cliente_ana.resumen())[1])

    # Operación 2 (Inválida): Registro de cliente con correo inválido
    def op_cliente_invalido():
        try:
            return Cliente("CLI-02", "Carlos Pérez", "correo_sin_arroba", "3112223344")
        except ValidacionEntidadError as e:
            raise OperacionReservaError("Fallo al crear ficha de cliente por datos inválidos.") from e  # Encadenamiento

    ejecutar_paso("Op 2: Registrar cliente con correo inválido (encadenamiento)", op_cliente_invalido)

    # Operación 3 (Válida): Crear servicio de Reserva de Sala
    sala_a = ReservaSala("SRV-SAL-1", "Sala Reuniones Norte", 50000, capacidad_maxima=10, disponible=True)
    ejecutar_paso("Op 3: Crear servicio de Sala", lambda: (gestor.registrar_servicio(sala_a), sala_a.resumen())[1])

    # Operación 4 (Válida): Crear servicio de Alquiler de Equipo
    laptop_srv = AlquilerEquipo("SRV-EQ-1", "Laptop Desarrollo i7", 25000, stock_disponible=5, disponible=True)
    ejecutar_paso("Op 4: Crear servicio de Alquiler de Equipo", lambda: (gestor.registrar_servicio(laptop_srv), laptop_srv.resumen())[1])

    # Operación 5 (Válida): Crear servicio de Asesoría Especializada
    asesoria_srv = AsesoriaEspecializada("SRV-ASE-1", "Asesoría Arquitectura Cloud", 120000, modalidad="Remota", disponible=True)
    ejecutar_paso("Op 5: Crear servicio de Asesoría", lambda: (gestor.registrar_servicio(asesoria_srv), asesoria_srv.resumen())[1])

    # Operación 6 (Inválida): Crear servicio con tarifa negativa
    ejecutar_paso("Op 6: Crear servicio con tarifa inválida", lambda: AsesoriaEspecializada("SRV-ERR", "Asesoría Inválida", -10000))

    # Operación 7 (Válida): Crear y confirmar reserva de sala con descuento e impuesto
    reserva_1 = Reserva("RES-101", cliente_ana, sala_a, duracion_horas=3, unidades=6)
    ejecutar_paso(
        "Op 7: Crear y confirmar reserva de sala",
        lambda: (gestor.crear_reserva(reserva_1), f"Total confirmado: ${reserva_1.confirmar(descuento_porcentaje=10, impuesto_porcentaje=19):,.2f}")[1]
    )

    # Operación 8 (Válida): Procesar reserva confirmada
    ejecutar_paso("Op 8: Procesar reserva confirmada RES-101", lambda: reserva_1.procesar())

    # Operación 9 (Inválida): Intentar cancelar una reserva ya procesada
    ejecutar_paso("Op 9: Cancelar reserva ya procesada RES-101", lambda: reserva_1.cancelar("Cambio de última hora"))

    # Operación 10 (Inválida): Reservar equipo excediendo stock disponible
    reserva_2 = Reserva("RES-102", cliente_ana, laptop_srv, duracion_horas=5, unidades=20)
    ejecutar_paso(
        "Op 10: Confirmar reserva de equipo sin stock suficiente",
        lambda: (gestor.crear_reserva(reserva_2), reserva_2.confirmar())[1]
    )

    # Operación 11 (Inválida): Reservar servicio marcado como no disponible
    asesoria_srv.cambiar_disponibilidad(False)  # Marca asesoría como no disponible
    reserva_3 = Reserva("RES-103", cliente_ana, asesoria_srv, duracion_horas=2, unidades=1)
    ejecutar_paso(
        "Op 11: Confirmar reserva sobre servicio no disponible",
        lambda: (gestor.crear_reserva(reserva_3), reserva_3.confirmar())[1]
    )

    # Operación 12 (Válida): Crear, confirmar y cancelar reserva pendiente correctamente
    asesoria_srv.cambiar_disponibilidad(True)  # Restaura disponibilidad del servicio
    reserva_4 = Reserva("RES-104", cliente_ana, asesoria_srv, duracion_horas=2, unidades=1)
    ejecutar_paso(
        "Op 12: Crear y cancelar reserva pendiente RES-104",
        lambda: (gestor.crear_reserva(reserva_4), reserva_4.cancelar("Reprogramación solicitada"), "RES-104 cancelada")[2]
    )

    print(f"\nSimulación finalizada. Operaciones exitosas: {operaciones_exitosas}/12. Revisa 'logs/sistema_software_fj.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()  # Ejecuta la simulación al correr el archivo directamente