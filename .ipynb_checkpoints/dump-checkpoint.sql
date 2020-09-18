--
-- PostgreSQL database dump
--

-- Dumped from database version 11.6 (Debian 11.6-1.pgdg90+1)
-- Dumped by pg_dump version 11.6 (Debian 11.6-1.pgdg90+1)

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

SET default_with_oids = false;

--
-- Name: exam; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam (
    id integer NOT NULL,
    duration integer
);


ALTER TABLE public.exam OWNER TO postgres;

--
-- Name: exam_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_id_seq OWNER TO postgres;

--
-- Name: exam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_id_seq OWNED BY public.exam.id;


--
-- Name: exam_period; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_period (
    id integer NOT NULL,
    exam_id integer,
    period_id integer
);


ALTER TABLE public.exam_period OWNER TO postgres;

--
-- Name: exam_period_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_period_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_period_id_seq OWNER TO postgres;

--
-- Name: exam_period_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_period_id_seq OWNED BY public.exam_period.id;


--
-- Name: exam_student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam_student (
    id integer NOT NULL,
    exam_id integer,
    student_id integer
);


ALTER TABLE public.exam_student OWNER TO postgres;

--
-- Name: exam_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exam_student_id_seq OWNER TO postgres;

--
-- Name: exam_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_student_id_seq OWNED BY public.exam_student.id;


--
-- Name: period; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.period (
    id integer NOT NULL,
    "time" timestamp without time zone,
    duration integer,
    penalty integer
);


ALTER TABLE public.period OWNER TO postgres;

--
-- Name: period_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.period_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.period_id_seq OWNER TO postgres;

--
-- Name: period_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.period_id_seq OWNED BY public.period.id;


--
-- Name: period_room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.period_room (
    id integer NOT NULL,
    period_id integer,
    room_id integer
);


ALTER TABLE public.period_room OWNER TO postgres;

--
-- Name: period_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.period_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.period_room_id_seq OWNER TO postgres;

--
-- Name: period_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.period_room_id_seq OWNED BY public.period_room.id;


--
-- Name: room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room (
    id integer NOT NULL,
    capacity integer,
    penalty integer
);


ALTER TABLE public.room OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_id_seq OWNER TO postgres;

--
-- Name: room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;


--
-- Name: staticheuristics; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.staticheuristics AS
 SELECT a.exam_id,
    b.student_id,
    b.exam_count,
    a.student_count
   FROM ( SELECT exam_student.exam_id,
            count(exam_student.student_id) AS student_count
           FROM public.exam_student
          GROUP BY exam_student.exam_id) a,
    ( SELECT exam_student.student_id,
            count(exam_student.exam_id) AS exam_count
           FROM public.exam_student
          GROUP BY exam_student.student_id) b
  ORDER BY b.exam_count DESC;


ALTER TABLE public.staticheuristics OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    id integer NOT NULL,
    number integer
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_id_seq OWNER TO postgres;

--
-- Name: student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_id_seq OWNED BY public.student.id;


--
-- Name: exam id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam ALTER COLUMN id SET DEFAULT nextval('public.exam_id_seq'::regclass);


--
-- Name: exam_period id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_period ALTER COLUMN id SET DEFAULT nextval('public.exam_period_id_seq'::regclass);


--
-- Name: exam_student id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_student ALTER COLUMN id SET DEFAULT nextval('public.exam_student_id_seq'::regclass);


--
-- Name: period id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period ALTER COLUMN id SET DEFAULT nextval('public.period_id_seq'::regclass);


--
-- Name: period_room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period_room ALTER COLUMN id SET DEFAULT nextval('public.period_room_id_seq'::regclass);


--
-- Name: room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);


--
-- Name: student id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN id SET DEFAULT nextval('public.student_id_seq'::regclass);


--
-- Data for Name: exam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam (id, duration) FROM stdin;
1	60
2	60
3	60
4	60
5	60
6	60
7	90
8	60
9	90
10	90
\.


--
-- Data for Name: exam_period; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_period (id, exam_id, period_id) FROM stdin;
1	6	3
2	9	1
3	7	3
4	3	5
5	8	4
6	4	5
7	2	1
8	5	6
9	1	2
10	10	1
\.


--
-- Data for Name: exam_student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam_student (id, exam_id, student_id) FROM stdin;
1	1	8
2	9	8
3	4	8
4	10	8
5	1	2
6	2	2
7	3	2
8	4	2
9	5	2
10	6	2
11	1	10
12	4	10
13	1	5
14	2	5
15	7	5
16	4	5
17	5	5
18	8	5
19	1	9
20	9	9
21	4	9
22	10	9
23	1	4
24	2	4
25	7	4
26	4	4
27	5	4
28	8	4
29	1	6
30	9	6
31	4	6
32	10	6
33	1	1
34	2	1
35	3	1
36	4	1
37	5	1
38	6	1
39	1	3
40	2	3
41	3	3
42	4	3
43	5	3
44	6	3
45	1	7
46	9	7
47	4	7
48	10	7
\.


--
-- Data for Name: period; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.period (id, "time", duration, penalty) FROM stdin;
1	2005-04-15 09:30:00	90	10
2	2005-04-15 14:00:00	90	0
3	2005-04-18 09:30:00	90	0
4	2005-04-18 14:00:00	90	0
5	2005-04-19 09:30:00	90	20
6	2005-04-20 09:30:00	90	0
\.


--
-- Data for Name: period_room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.period_room (id, period_id, room_id) FROM stdin;
1	1	1
2	6	1
3	4	1
4	3	1
5	2	2
6	5	2
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room (id, capacity, penalty) FROM stdin;
1	10	20
2	10	10
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (id, number) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- Name: exam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_id_seq', 10, true);


--
-- Name: exam_period_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_period_id_seq', 10, true);


--
-- Name: exam_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_student_id_seq', 48, true);


--
-- Name: period_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.period_id_seq', 6, true);


--
-- Name: period_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.period_room_id_seq', 6, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.room_id_seq', 2, true);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_id_seq', 10, true);


--
-- Name: exam_period exam_period_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_period
    ADD CONSTRAINT exam_period_pkey PRIMARY KEY (id);


--
-- Name: exam exam_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_pkey PRIMARY KEY (id);


--
-- Name: exam_student exam_student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_student
    ADD CONSTRAINT exam_student_pkey PRIMARY KEY (id);


--
-- Name: period period_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period
    ADD CONSTRAINT period_pkey PRIMARY KEY (id);


--
-- Name: period_room period_room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period_room
    ADD CONSTRAINT period_room_pkey PRIMARY KEY (id);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);


--
-- Name: exam_period exam_period_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_period
    ADD CONSTRAINT exam_period_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON DELETE CASCADE;


--
-- Name: exam_period exam_period_period_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_period
    ADD CONSTRAINT exam_period_period_id_fkey FOREIGN KEY (period_id) REFERENCES public.period(id) ON DELETE CASCADE;


--
-- Name: exam_student exam_student_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_student
    ADD CONSTRAINT exam_student_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON DELETE CASCADE;


--
-- Name: exam_student exam_student_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_student
    ADD CONSTRAINT exam_student_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(id) ON DELETE CASCADE;


--
-- Name: period_room period_room_period_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period_room
    ADD CONSTRAINT period_room_period_id_fkey FOREIGN KEY (period_id) REFERENCES public.period(id) ON DELETE CASCADE;


--
-- Name: period_room period_room_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.period_room
    ADD CONSTRAINT period_room_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

