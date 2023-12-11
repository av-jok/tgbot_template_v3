--
-- PostgreSQL database dump
--

-- Dumped from database version 13.12
-- Dumped by pg_dump version 13.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: joker
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO joker;

--
-- Name: photos; Type: TABLE; Schema: public; Owner: joker
--

CREATE TABLE public.photos (
    id bigint NOT NULL,
    sid bigint NOT NULL,
    tid character varying(128),
    name character varying(128),
    file_id character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.photos OWNER TO joker;

--
-- Name: photos_id_seq; Type: SEQUENCE; Schema: public; Owner: joker
--

CREATE SEQUENCE public.photos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.photos_id_seq OWNER TO joker;

--
-- Name: photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: joker
--

ALTER SEQUENCE public.photos_id_seq OWNED BY public.photos.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: joker
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    username character varying(128),
    full_name character varying(128) NOT NULL,
    active boolean DEFAULT true NOT NULL,
    language character varying(10) DEFAULT 'en'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO joker;

--
-- Name: photos id; Type: DEFAULT; Schema: public; Owner: joker
--

ALTER TABLE ONLY public.photos ALTER COLUMN id SET DEFAULT nextval('public.photos_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: joker
--

COPY public.alembic_version (version_num) FROM stdin;
2bcd53e28abe
\.


--
-- Data for Name: photos; Type: TABLE DATA; Schema: public; Owner: joker
--

COPY public.photos (id, sid, tid, name, file_id, created_at) FROM stdin;
1	22222	55555	ssfgfgs	dsfgdgsdfg	2023-10-19 17:24:37.702378
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: joker
--

COPY public.users (user_id, username, full_name, active, language, created_at) FROM stdin;
\.


--
-- Name: photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: joker
--

SELECT pg_catalog.setval('public.photos_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: joker
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: joker
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (id, sid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: joker
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- PostgreSQL database dump complete
--

