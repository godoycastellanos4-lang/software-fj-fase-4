Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

Curso: Programación (213023) – UNAD

Actividad: Fase 4 – Componente Práctico (Prácticas Simuladas)

Modalidad: Desarrollo individual (ante ausencia de participación grupal en el foro)

Descripción del Proyecto

Aplicación desarrollada en Python 3 bajo el paradigma de Programación Orientada a Objetos (POO) sin uso de bases de datos. El sistema gestiona en memoria clientes, servicios especializados y reservas para la empresa Software FJ, garantizando estabilidad y continuidad operativa mediante un esquema avanzado de manejo de excepciones y auditoría en archivos de registro (.log).

Características Técnicas Implementadas

Abstracción y Herencia:

EntidadBase (clase abstracta): define atributos comunes (identificador, nombre, fecha de creación) y validaciones base.

Servicio (clase abstracta): establece el contrato de validación de parámetros y cálculo de costos para el portafolio de Software FJ.

Encapsulación:

Cliente: protege los datos personales (__correo, __telefono) mediante propiedades (@property) y setters con validación estricta.

Polimorfismo y Sobrecarga:

Subclases especializadas ReservaSala, AlquilerEquipo y AsesoriaEspecializada con reglas propias de validación y cálculo base.

Método calcular_costo(...) con parámetros opcionales (cantidad_unidades, descuento_porcentaje, impuesto_porcentaje).

Gestión de Reservas:

Reserva: administra el ciclo de vida (PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA) y el procesamiento seguro.

Manejo Avanzado de Excepciones y Logs:

Excepciones personalizadas (ErrorSoftwareFJ, ValidacionEntidadError, ServicioNoDisponibleError, OperacionReservaError, CalculoFinancieroError).

Uso de bloques try / except / else / finally y encadenamiento de excepciones (raise ... from ...).

Registro automático de eventos exitosos y errores controlados en logs/sistema_software_fj.log.

Estructura del Repositorio

├── prog4.py                        # Código fuente principal documentado línea por línea
├── README.md                      # Documentación general del proyecto
└── logs/
    └── sistema_software_fj.log    # Archivo de registro generado tras la simulación
