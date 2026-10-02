--
-- PostgreSQL database dump
--

\restrict qPdU2hsuPIlDgnsgXTCaKYKlbBbfjG1euDzhrBcAQqDqq4KwdOPqaE85gRpaSHM

-- Dumped from database version 18.6 (Debian 18.6-1.pgdg12+2)
-- Dumped by pg_dump version 18.6 (Debian 18.6-1.pgdg12+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: usuario
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO usuario;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agenda; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.agenda (
    id_agenda integer NOT NULL,
    fecha_programada date NOT NULL,
    id_ente integer NOT NULL,
    actividad text NOT NULL,
    objetivo text,
    descripcion text,
    creado_por_id integer,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.agenda OWNER TO usuario;

--
-- Name: agenda_id_agenda_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.agenda_id_agenda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agenda_id_agenda_seq OWNER TO usuario;

--
-- Name: agenda_id_agenda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.agenda_id_agenda_seq OWNED BY public.agenda.id_agenda;


--
-- Name: cargos; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.cargos (
    id_cargo integer NOT NULL,
    nombre_cargo character varying(100) NOT NULL
);


ALTER TABLE public.cargos OWNER TO usuario;

--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.cargos_id_cargo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cargos_id_cargo_seq OWNER TO usuario;

--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.cargos_id_cargo_seq OWNED BY public.cargos.id_cargo;


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nombre_categoria character varying(100) NOT NULL
);


ALTER TABLE public.categorias OWNER TO usuario;

--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categorias_id_categoria_seq OWNER TO usuario;

--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.categorias_id_categoria_seq OWNED BY public.categorias.id_categoria;


--
-- Name: entes; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.entes (
    id_ente integer NOT NULL,
    nombre_ente character varying(255) NOT NULL,
    direccion text,
    comuna character varying(150),
    latitud numeric(10,8),
    longitud numeric(11,8),
    kids_fem numeric DEFAULT 0,
    kids_mas numeric DEFAULT 0,
    joven_fem numeric DEFAULT 0,
    joven_mas numeric DEFAULT 0,
    mujer numeric DEFAULT 0,
    hombre numeric DEFAULT 0,
    am_fem numeric DEFAULT 0,
    am_mas numeric DEFAULT 0
);


ALTER TABLE public.entes OWNER TO usuario;

--
-- Name: entes_id_ente_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.entes_id_ente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entes_id_ente_seq OWNER TO usuario;

--
-- Name: entes_id_ente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.entes_id_ente_seq OWNED BY public.entes.id_ente;


--
-- Name: historial_autoridades; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.historial_autoridades (
    id_auto integer NOT NULL,
    id_ente integer NOT NULL,
    nombre_auto character varying(150) NOT NULL,
    cargo_auto character varying(100),
    celular_auto character varying(20),
    telef_auto character varying(20),
    email_auto character varying(100),
    activo_auto boolean DEFAULT true
);


ALTER TABLE public.historial_autoridades OWNER TO usuario;

--
-- Name: historial_autoridades_id_auto_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.historial_autoridades_id_auto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historial_autoridades_id_auto_seq OWNER TO usuario;

--
-- Name: historial_autoridades_id_auto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.historial_autoridades_id_auto_seq OWNED BY public.historial_autoridades.id_auto;


--
-- Name: historial_contactos; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.historial_contactos (
    id_cont integer NOT NULL,
    id_ente integer NOT NULL,
    nombre_cont character varying(150),
    cargo_cont character varying(100),
    celular_cont character varying(20),
    telef_cont character varying(20),
    email_cont character varying(100),
    activo_cont boolean DEFAULT true
);


ALTER TABLE public.historial_contactos OWNER TO usuario;

--
-- Name: historial_contactos_id_cont_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.historial_contactos_id_cont_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historial_contactos_id_cont_seq OWNER TO usuario;

--
-- Name: historial_contactos_id_cont_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.historial_contactos_id_cont_seq OWNED BY public.historial_contactos.id_cont;


--
-- Name: logs_sistema; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.logs_sistema (
    id_log integer NOT NULL,
    id_tecnico integer,
    accion character varying(100) NOT NULL,
    detalles text,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.logs_sistema OWNER TO usuario;

--
-- Name: logs_sistema_id_log_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.logs_sistema_id_log_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_sistema_id_log_seq OWNER TO usuario;

--
-- Name: logs_sistema_id_log_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.logs_sistema_id_log_seq OWNED BY public.logs_sistema.id_log;


--
-- Name: reporte; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    codigo_equipo character varying(20),
    fecha_servicio date NOT NULL,
    id_ente integer NOT NULL,
    id_tecnico integer NOT NULL,
    id_tipo integer NOT NULL,
    piso character varying(50),
    departamento character varying(150),
    marca character varying(100),
    modelo character varying(100),
    serial character varying(100),
    nro_bien_nacional character varying(100),
    estatus_inicial character varying(50) NOT NULL,
    estatus_final character varying(50) NOT NULL,
    tipo_mantenimiento character varying(50),
    observaciones_accion text,
    descripcion_falla text,
    foto_chapa character varying(255),
    foto_falla character varying(255),
    foto_trabajo character varying(255),
    creado_por_id integer,
    creado_en timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reporte OWNER TO usuario;

--
-- Name: reporte_id_reporte_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.reporte_id_reporte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reporte_id_reporte_seq OWNER TO usuario;

--
-- Name: reporte_id_reporte_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.reporte_id_reporte_seq OWNED BY public.reporte.id_reporte;


--
-- Name: seq_codigo_equipo; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.seq_codigo_equipo
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_codigo_equipo OWNER TO usuario;

--
-- Name: tecnicos; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.tecnicos (
    id_tecnico integer NOT NULL,
    nombre_tecnico character varying(100) NOT NULL,
    usuario character varying(50),
    password_hash character varying(255),
    rol character varying(20) DEFAULT 'tecnico'::character varying,
    activo boolean DEFAULT true
);


ALTER TABLE public.tecnicos OWNER TO usuario;

--
-- Name: tecnicos_id_tecnico_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.tecnicos_id_tecnico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tecnicos_id_tecnico_seq OWNER TO usuario;

--
-- Name: tecnicos_id_tecnico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.tecnicos_id_tecnico_seq OWNED BY public.tecnicos.id_tecnico;


--
-- Name: tipos_equipo; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.tipos_equipo (
    id_tipo integer NOT NULL,
    id_categoria integer NOT NULL,
    nombre_tipo character varying(100) NOT NULL
);


ALTER TABLE public.tipos_equipo OWNER TO usuario;

--
-- Name: tipos_equipo_id_tipo_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.tipos_equipo_id_tipo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_equipo_id_tipo_seq OWNER TO usuario;

--
-- Name: tipos_equipo_id_tipo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.tipos_equipo_id_tipo_seq OWNED BY public.tipos_equipo.id_tipo;


--
-- Name: agenda id_agenda; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.agenda ALTER COLUMN id_agenda SET DEFAULT nextval('public.agenda_id_agenda_seq'::regclass);


--
-- Name: cargos id_cargo; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.cargos ALTER COLUMN id_cargo SET DEFAULT nextval('public.cargos_id_cargo_seq'::regclass);


--
-- Name: categorias id_categoria; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.categorias_id_categoria_seq'::regclass);


--
-- Name: entes id_ente; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.entes ALTER COLUMN id_ente SET DEFAULT nextval('public.entes_id_ente_seq'::regclass);


--
-- Name: historial_autoridades id_auto; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_autoridades ALTER COLUMN id_auto SET DEFAULT nextval('public.historial_autoridades_id_auto_seq'::regclass);


--
-- Name: historial_contactos id_cont; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_contactos ALTER COLUMN id_cont SET DEFAULT nextval('public.historial_contactos_id_cont_seq'::regclass);


--
-- Name: logs_sistema id_log; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.logs_sistema ALTER COLUMN id_log SET DEFAULT nextval('public.logs_sistema_id_log_seq'::regclass);


--
-- Name: reporte id_reporte; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte ALTER COLUMN id_reporte SET DEFAULT nextval('public.reporte_id_reporte_seq'::regclass);


--
-- Name: tecnicos id_tecnico; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tecnicos ALTER COLUMN id_tecnico SET DEFAULT nextval('public.tecnicos_id_tecnico_seq'::regclass);


--
-- Name: tipos_equipo id_tipo; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tipos_equipo ALTER COLUMN id_tipo SET DEFAULT nextval('public.tipos_equipo_id_tipo_seq'::regclass);


--
-- Data for Name: agenda; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.agenda (id_agenda, fecha_programada, id_ente, actividad, objetivo, descripcion, creado_por_id, creado_en) FROM stdin;
1	2026-05-22	1	Formación Docente del Programa Pequeños Ingenieros del Programa Nacional de  "Semilleros Científico"	Módulo I  Kit Educativo Pequeños Ingenieros\n[24/5, 11:54 a. m.] Ing Richard Torrealba: 🛰️ FUNDACITE COJEDES - MINCYT\n🛠️ PLAN CAYAPA HEROICA	\N	\N	2026-07-29 00:20:14.857967
2	2026-05-25	2	Validar la compatibilidad técnica de equipos de computación	Instalar el sistema operativo GNU/Linux Canaima 8.3 "Semillero Científico"	\N	\N	2026-07-29 00:20:14.857967
3	2026-07-28	1	VISITAR LABORATORIO DE QUÍMICA ORGÁNICA	EVALUAR ESTADO DE LOS EQUIPOS DE MEDICIÓN DEL LABORATORIO.	\N	\N	2026-07-29 00:20:14.857967
\.


--
-- Data for Name: cargos; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.cargos (id_cargo, nombre_cargo) FROM stdin;
1	Director (a)
2	Coordinador(a)
3	Administrador(a)
4	Gerente(a)
5	Obrero(a)
6	Secretario(a)
7	Asistente
8	Seguridad
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.categorias (id_categoria, nombre_categoria) FROM stdin;
1	Equipos Informáticos
2	Climatización / Refrigeración
3	Equipos Médicos
4	Electrodomésticos
\.


--
-- Data for Name: entes; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.entes (id_ente, nombre_ente, direccion, comuna, latitud, longitud, kids_fem, kids_mas, joven_fem, joven_mas, mujer, hombre, am_fem, am_mas) FROM stdin;
1	Complejo Educativo Andrés Benito Espinoza	Urb, la Herrereña, calle 10 sector2, San Carlos, Cojedes.	Revolución Zamorana	9.64861700	-68.56644200	0	90	0	95	335	310	0	0
2	Centro de Recursos para los Aprendizajes	Urbanización La Herreñera II, Sector I, Calle 10, San Carlos	Revolucion Zamorana	9.64836100	-68.56680600	1702	3677	0	0	2136	1536	0	0
3	FUNDACITE COJEDES	AV BOLÍVAR EN CALLE MANRIQUE Y  SILVA, SAN CARLOS	GIGANTE DE AMERICA	9.66217400	-68.59167300	0	0	0	0	24	24	0	0
\.


--
-- Data for Name: historial_autoridades; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.historial_autoridades (id_auto, id_ente, nombre_auto, cargo_auto, celular_auto, telef_auto, email_auto, activo_auto) FROM stdin;
1	1	Aury Meléndez	Director(a)	0412xxxxxxx	0258xxxxxxx	xxxxxxxa@hotmail.com	t
2	2	Audri Meléndez	Coordinador(a)	0422789xxxx	\N	\N	t
3	3	PABLO RODRIGUEZ	Director (a)	04144027710	02584335946	mincytcojedes@gmail.com	t
\.


--
-- Data for Name: historial_contactos; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.historial_contactos (id_cont, id_ente, nombre_cont, cargo_cont, celular_cont, telef_cont, email_cont, activo_cont) FROM stdin;
1	1	contacto contacto	Enlace Operativo	0412xxxxxxx	0258xxxxxxx	contacto@hotmail.com	t
2	3	RAMÓN FRANCO	Coordinador(a)	04124567845	02584335946	MINCYTCOJEDES@GMAIL.COM	t
\.


--
-- Data for Name: logs_sistema; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.logs_sistema (id_log, id_tecnico, accion, detalles, fecha) FROM stdin;
\.


--
-- Data for Name: reporte; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.reporte (id_reporte, codigo_equipo, fecha_servicio, id_ente, id_tecnico, id_tipo, piso, departamento, marca, modelo, serial, nro_bien_nacional, estatus_inicial, estatus_final, tipo_mantenimiento, observaciones_accion, descripcion_falla, foto_chapa, foto_falla, foto_trabajo, creado_por_id, creado_en) FROM stdin;
1	CH-COJ-000037	2026-07-28	2	5	10	planta baja	Servicios generales	Frigilux	amx300	123456	BN-123456	Revisado – Inoperativa	Reparado	Correctivo	Cargas de gas y limpieza profunda	Capacitadores quemados, colmenas sucias, presión de gas refrigerante baja.	static/uploads/CH-COJ-000037_chapa.jpg	static/uploads/CH-COJ-000037_falla.jpg	static/uploads/CH-COJ-000037_trabajo.jpg	\N	2026-07-29 00:20:14.850015
2	CH-COJ-000038	2026-07-28	1	5	10	PLANTA BAJA	SALA DE CIENCIA	FRIGILUX	AMX-30	SN-457812-LAT	BN-457812-LAT	Revisado – Inoperativa	Reparado	Correctivo	REMPLAZO DE CAPACITO DE ARRANQUE, LIPIEZA PROFUNDA DE COLMENA, RECARGA DE GAS REFRIGERANTE	CAPACITADOR DE ARRANQUE DAÑADO,COLMENAS SUCIA, BAJA ŔESIÓN DE GAS REFRIGERANTE.	static/uploads/CH-COJ-000038_chapa.jpg	static/uploads/CH-COJ-000038_falla.jpg	static/uploads/CH-COJ-000038_trabajo.jpg	\N	2026-07-29 00:20:14.850015
\.


--
-- Data for Name: tecnicos; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.tecnicos (id_tecnico, nombre_tecnico, usuario, password_hash, rol, activo) FROM stdin;
4	RICHARD TORREALBA	rtorrealba	$2b$12$Us8bSTVpv7xIQEb4LZj0SOE/q7V7LH4r7xXT5PK2a2ORKzpGOCaCW	admin	t
1	VICTOR MELENDEZ	victor1	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
2	EUDIS AGUILERA	eudis2	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
3	ANABEL ALVARADO	anabel3	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
5	ANA VILLEGAS	ana5	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
6	DOUGLAS PETIT	douglas6	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
7	FREDDY BERNAL	freddy7	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
8	JOSE GUTIERREZ	jose8	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
9	CESAR SANCHEZ	cesar9	$2b$12$J1hzOZfEKS9HuhWAGv3JYewb6RGs7IDcaPGwiP4VEno48P.ZgTPVa	tecnico	t
\.


--
-- Data for Name: tipos_equipo; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.tipos_equipo (id_tipo, id_categoria, nombre_tipo) FROM stdin;
1	1	PC
2	1	SERVIDOR
3	1	ROUTER
4	1	SWICHT
5	1	REGULADOR DE VOLTAGE
6	1	MONITOR
7	1	TECLADO
8	1	MAUSE
9	2	AIRES ACONDICONADO VENTANA
10	2	AIRES ACONDICONADO SPLIT
11	2	VENTILADOR
12	2	DESHUMIDIFICADOR
13	2	NEVERA
14	2	CONGELADOR
15	2	CAVA
16	2	CAVA CUARTO
17	2	ENFRIADOR DE AGUA
18	3	NEGATOSCOPIO
19	3	SISTEMA RX
20	3	SISTEMA RESONANCIA ELECTROMAGNETICA
21	3	SISTEMA DE IMAGENOLOGIA
22	3	SILLA ODONTOLOGICA
23	3	HORNO ESTERILIZACION
24	3	CAMARA DE GAS
25	3	ESTERILIZADORES UV
26	3	BALANZAS
27	3	TENSIOMETRO
28	3	NEBULIZADOR
29	3	OTOCOSPIO
30	3	AUTOCLAVE
31	3	Extractor de Flema
32	4	LUMINARIAS
33	4	CAFETERA
34	4	HORNO MICRO HONDAS
35	4	HORNO ELECTRICO
36	4	VETILADOR
\.


--
-- Name: agenda_id_agenda_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.agenda_id_agenda_seq', 3, true);


--
-- Name: cargos_id_cargo_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.cargos_id_cargo_seq', 8, true);


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.categorias_id_categoria_seq', 5, true);


--
-- Name: entes_id_ente_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.entes_id_ente_seq', 3, true);


--
-- Name: historial_autoridades_id_auto_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.historial_autoridades_id_auto_seq', 3, true);


--
-- Name: historial_contactos_id_cont_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.historial_contactos_id_cont_seq', 2, true);


--
-- Name: logs_sistema_id_log_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.logs_sistema_id_log_seq', 1, false);


--
-- Name: reporte_id_reporte_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.reporte_id_reporte_seq', 2, true);


--
-- Name: seq_codigo_equipo; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.seq_codigo_equipo', 38, true);


--
-- Name: tecnicos_id_tecnico_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.tecnicos_id_tecnico_seq', 9, true);


--
-- Name: tipos_equipo_id_tipo_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.tipos_equipo_id_tipo_seq', 42, true);


--
-- Name: agenda agenda_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.agenda
    ADD CONSTRAINT agenda_pkey PRIMARY KEY (id_agenda);


--
-- Name: cargos cargos_nombre_cargo_key; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_nombre_cargo_key UNIQUE (nombre_cargo);


--
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.cargos
    ADD CONSTRAINT cargos_pkey PRIMARY KEY (id_cargo);


--
-- Name: categorias categorias_nombre_categoria_key; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_nombre_categoria_key UNIQUE (nombre_categoria);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- Name: entes entes_nombre_ente_key; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.entes
    ADD CONSTRAINT entes_nombre_ente_key UNIQUE (nombre_ente);


--
-- Name: entes entes_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.entes
    ADD CONSTRAINT entes_pkey PRIMARY KEY (id_ente);


--
-- Name: historial_autoridades historial_autoridades_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_autoridades
    ADD CONSTRAINT historial_autoridades_pkey PRIMARY KEY (id_auto);


--
-- Name: historial_contactos historial_contactos_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_contactos
    ADD CONSTRAINT historial_contactos_pkey PRIMARY KEY (id_cont);


--
-- Name: logs_sistema logs_sistema_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.logs_sistema
    ADD CONSTRAINT logs_sistema_pkey PRIMARY KEY (id_log);


--
-- Name: reporte reporte_codigo_equipo_key; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_codigo_equipo_key UNIQUE (codigo_equipo);


--
-- Name: reporte reporte_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (id_reporte);


--
-- Name: tecnicos tecnicos_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tecnicos
    ADD CONSTRAINT tecnicos_pkey PRIMARY KEY (id_tecnico);


--
-- Name: tecnicos tecnicos_usuario_key; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tecnicos
    ADD CONSTRAINT tecnicos_usuario_key UNIQUE (usuario);


--
-- Name: tipos_equipo tipos_equipo_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tipos_equipo
    ADD CONSTRAINT tipos_equipo_pkey PRIMARY KEY (id_tipo);


--
-- Name: agenda agenda_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.agenda
    ADD CONSTRAINT agenda_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES public.tecnicos(id_tecnico);


--
-- Name: agenda fk_agenda_ente; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.agenda
    ADD CONSTRAINT fk_agenda_ente FOREIGN KEY (id_ente) REFERENCES public.entes(id_ente) ON DELETE RESTRICT;


--
-- Name: historial_autoridades fk_autoridad_ente; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_autoridades
    ADD CONSTRAINT fk_autoridad_ente FOREIGN KEY (id_ente) REFERENCES public.entes(id_ente) ON DELETE CASCADE;


--
-- Name: historial_contactos fk_contacto_ente; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.historial_contactos
    ADD CONSTRAINT fk_contacto_ente FOREIGN KEY (id_ente) REFERENCES public.entes(id_ente) ON DELETE CASCADE;


--
-- Name: reporte fk_reporte_ente; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT fk_reporte_ente FOREIGN KEY (id_ente) REFERENCES public.entes(id_ente) ON DELETE RESTRICT;


--
-- Name: reporte fk_reporte_tecnico; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT fk_reporte_tecnico FOREIGN KEY (id_tecnico) REFERENCES public.tecnicos(id_tecnico) ON DELETE RESTRICT;


--
-- Name: reporte fk_reporte_tipo; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT fk_reporte_tipo FOREIGN KEY (id_tipo) REFERENCES public.tipos_equipo(id_tipo) ON DELETE RESTRICT;


--
-- Name: tipos_equipo fk_tipo_categoria; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.tipos_equipo
    ADD CONSTRAINT fk_tipo_categoria FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria) ON DELETE RESTRICT;


--
-- Name: logs_sistema logs_sistema_id_tecnico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.logs_sistema
    ADD CONSTRAINT logs_sistema_id_tecnico_fkey FOREIGN KEY (id_tecnico) REFERENCES public.tecnicos(id_tecnico);


--
-- Name: reporte reporte_creado_por_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_creado_por_id_fkey FOREIGN KEY (creado_por_id) REFERENCES public.tecnicos(id_tecnico);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO usuario;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO usuario;


--
-- PostgreSQL database dump complete
--

\unrestrict qPdU2hsuPIlDgnsgXTCaKYKlbBbfjG1euDzhrBcAQqDqq4KwdOPqaE85gRpaSHM

