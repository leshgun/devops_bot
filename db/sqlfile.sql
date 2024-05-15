--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Debian 15.6-0+deb12u1)
-- Dumped by pg_dump version 15.6 (Debian 15.6-0+deb12u1)

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
-- Name: email; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email (
    id integer NOT NULL,
    email character varying(355) NOT NULL
);


ALTER TABLE public.email OWNER TO postgres;

--
-- Name: email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.email_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_id_seq OWNER TO postgres;

--
-- Name: email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.email_id_seq OWNED BY public.email.id;


--
-- Name: phone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phone (
    id integer NOT NULL,
    phone text NOT NULL
);


ALTER TABLE public.phone OWNER TO postgres;

--
-- Name: phone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phone_id_seq OWNER TO postgres;

--
-- Name: phone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phone_id_seq OWNED BY public.phone.id;


--
-- Name: email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email ALTER COLUMN id SET DEFAULT nextval('public.email_id_seq'::regclass);


--
-- Name: phone id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone ALTER COLUMN id SET DEFAULT nextval('public.phone_id_seq'::regclass);


--
-- Data for Name: email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.email (id, email) FROM stdin;
1	abba@ab.ba
2	baab@ba.ab
3	test@mail.ru
4	gotebe_kapu76@outlook.com
5	kagagi_poxu66@hotmail.com
6	gac-udahici7@aol.com
7	ricofi-mozi35@yahoo.com
8	lul_efeseku79@outlook.com
9	cet_alayoho68@outlook.com
10	bak_osucucu93@mail.com
11	vep-asenoni63@yahoo.com
12	cumu-cafogi84@aol.com
13	busos_ijuxe71@gmail.com
14	testtest@test.ru
15	test7@mail.ru
16	test8@mail.ru
\.


--
-- Data for Name: phone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phone (id, phone) FROM stdin;
1	+7(4812)686262
2	+7(4742)895077
3	+7(383)3343775
4	+7(866)2777442
5	+7(863)2710103
6	+7(351)7567749
7	+7(861)7921744
8	+7(347)8273395
9	+7(495)4819109
11	+7(351)7567750
12	88005553535
\.


--
-- Name: email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.email_id_seq', 16, true);


--
-- Name: phone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phone_id_seq', 14, true);


--
-- Name: email email_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email
    ADD CONSTRAINT email_email_key UNIQUE (email);


--
-- Name: email email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email
    ADD CONSTRAINT email_pkey PRIMARY KEY (id);


--
-- Name: phone phone_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_phone_key UNIQUE (phone);


--
-- Name: phone phone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone
    ADD CONSTRAINT phone_pkey PRIMARY KEY (id);


--
-- Name: TABLE email; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.email TO master;


--
-- Name: SEQUENCE email_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.email_id_seq TO master;


--
-- Name: TABLE phone; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.phone TO master;


--
-- Name: SEQUENCE phone_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.phone_id_seq TO master;


--
-- PostgreSQL database dump complete
--

