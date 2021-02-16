--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.5

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

--
-- Name: loaninfo; Type: SCHEMA; Schema: -; Owner: poggers
--

CREATE SCHEMA loaninfo;


ALTER SCHEMA loaninfo OWNER TO poggers;

--
-- Name: event_type; Type: TYPE; Schema: public; Owner: poggers
--

CREATE TYPE public.event_type AS ENUM (
    'fee',
    'interest',
    'payment'
);


ALTER TYPE public.event_type OWNER TO poggers;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: loans; Type: TABLE; Schema: loaninfo; Owner: poggers
--

CREATE TABLE loaninfo.loans (
    index bigint,
    "1" bigint,
    "2019-12-17" text,
    "362.00" double precision
);


ALTER TABLE loaninfo.loans OWNER TO poggers;

--
-- Name: loan_events; Type: TABLE; Schema: public; Owner: poggers
--

CREATE TABLE public.loan_events (
    loan_id integer,
    event_type public.event_type,
    post_date date,
    amt numeric,
    tx_id integer NOT NULL
);


ALTER TABLE public.loan_events OWNER TO poggers;

--
-- Name: loan_events_tx_id_seq; Type: SEQUENCE; Schema: public; Owner: poggers
--

CREATE SEQUENCE public.loan_events_tx_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.loan_events_tx_id_seq OWNER TO poggers;

--
-- Name: loan_events_tx_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poggers
--

ALTER SEQUENCE public.loan_events_tx_id_seq OWNED BY public.loan_events.tx_id;


--
-- Name: loans; Type: TABLE; Schema: public; Owner: poggers
--

CREATE TABLE public.loans (
    loan_id integer NOT NULL,
    start_date date,
    initial_amt numeric
);


ALTER TABLE public.loans OWNER TO poggers;

--
-- Name: loans_loan_id_seq; Type: SEQUENCE; Schema: public; Owner: poggers
--

CREATE SEQUENCE public.loans_loan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.loans_loan_id_seq OWNER TO poggers;

--
-- Name: loans_loan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poggers
--

ALTER SEQUENCE public.loans_loan_id_seq OWNED BY public.loans.loan_id;


--
-- Name: ttest; Type: TABLE; Schema: public; Owner: poggers
--

CREATE TABLE public.ttest (
    id integer NOT NULL,
    value integer
);


ALTER TABLE public.ttest OWNER TO poggers;

--
-- Name: ttest_id_seq; Type: SEQUENCE; Schema: public; Owner: poggers
--

CREATE SEQUENCE public.ttest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ttest_id_seq OWNER TO poggers;

--
-- Name: ttest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poggers
--

ALTER SEQUENCE public.ttest_id_seq OWNED BY public.ttest.id;


--
-- Name: loan_events tx_id; Type: DEFAULT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.loan_events ALTER COLUMN tx_id SET DEFAULT nextval('public.loan_events_tx_id_seq'::regclass);


--
-- Name: loans loan_id; Type: DEFAULT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.loans ALTER COLUMN loan_id SET DEFAULT nextval('public.loans_loan_id_seq'::regclass);


--
-- Name: ttest id; Type: DEFAULT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.ttest ALTER COLUMN id SET DEFAULT nextval('public.ttest_id_seq'::regclass);


--
-- Data for Name: loans; Type: TABLE DATA; Schema: loaninfo; Owner: poggers
--

COPY loaninfo.loans (index, "1", "2019-12-17", "362.00") FROM stdin;
0	2	2019-12-07	483
1	3	2019-12-15	282
2	4	2019-12-27	150
3	5	2019-12-31	219
4	6	2019-12-25	369
5	7	2019-12-16	200
6	8	2019-12-15	65
7	9	2019-12-08	393
8	10	2019-12-05	351
\.


--
-- Data for Name: loan_events; Type: TABLE DATA; Schema: public; Owner: poggers
--

COPY public.loan_events (loan_id, event_type, post_date, amt, tx_id) FROM stdin;
1	payment	2020-08-15	80.00	1
2	payment	2020-03-26	72.00	2
2	fee	2020-03-25	33.00	3
8	fee	2020-03-24	46.00	4
7	payment	2020-05-29	47.00	5
2	fee	2020-02-26	78.00	6
10	fee	2020-03-17	89.00	7
2	fee	2020-11-17	48.00	8
5	interest	2020-08-29	60.00	9
2	payment	2020-09-11	63.00	10
9	payment	2020-03-24	80.00	11
4	interest	2020-04-04	99.00	12
7	fee	2020-10-30	61.00	13
8	interest	2020-11-17	11.00	14
3	interest	2020-11-14	51.00	15
1	payment	2020-10-02	7.00	16
8	fee	2020-04-12	90.00	17
5	fee	2020-04-17	20.00	18
8	payment	2020-07-23	25.00	19
8	fee	2020-07-12	96.00	20
1	interest	2020-08-12	1.00	21
10	interest	2020-08-02	36.00	22
3	payment	2020-10-05	97.00	23
6	interest	2020-07-05	74.00	24
7	payment	2020-11-23	62.00	25
9	fee	2020-05-04	30.00	26
9	payment	2020-04-27	95.00	27
7	payment	2020-05-18	80.00	28
8	fee	2020-01-10	5.00	29
5	payment	2020-04-30	3.00	30
8	payment	2020-10-28	81.00	31
1	payment	2020-04-24	57.00	32
5	interest	2020-02-17	81.00	33
1	interest	2020-02-24	38.00	34
6	payment	2020-08-27	40.00	35
9	fee	2020-11-18	11.00	36
6	interest	2020-10-07	79.00	37
9	payment	2020-07-01	4.00	38
9	payment	2020-05-08	13.00	39
8	payment	2020-07-28	17.00	40
7	interest	2020-05-17	23.00	41
9	fee	2020-12-14	91.00	42
10	payment	2020-06-28	38.00	43
9	interest	2020-02-04	42.00	44
10	interest	2020-06-02	91.00	45
4	interest	2020-07-28	35.00	46
6	fee	2020-06-08	89.00	47
5	fee	2020-11-10	48.00	48
3	interest	2020-03-04	93.00	49
9	fee	2020-05-14	65.00	50
2	interest	2020-12-30	52.00	51
7	fee	2020-06-18	12.00	52
2	fee	2020-01-26	38.00	53
1	payment	2020-07-14	34.00	54
7	payment	2020-04-14	12.00	55
2	fee	2020-07-15	13.00	56
5	payment	2020-08-29	4.00	57
9	interest	2020-04-16	21.00	58
6	fee	2020-03-31	19.00	59
1	interest	2020-09-24	12.00	60
4	fee	2020-10-05	59.00	61
8	payment	2020-05-17	4.00	62
2	interest	2020-01-09	60.00	63
2	interest	2020-03-21	20.00	64
8	payment	2020-02-09	5.00	65
1	interest	2020-08-07	84.00	66
1	fee	2020-06-25	21.00	67
1	fee	2020-10-10	50.00	68
6	fee	2020-06-23	63.00	69
10	fee	2020-07-04	89.00	70
1	interest	2020-08-12	93.00	71
5	payment	2020-07-02	99.00	72
6	interest	2020-12-08	30.00	73
2	interest	2020-01-31	75.00	74
5	interest	2020-05-18	58.00	75
4	fee	2020-01-03	24.00	76
7	fee	2020-10-17	32.00	77
7	fee	2020-05-21	70.00	78
10	payment	2020-06-16	99.00	79
7	fee	2020-07-05	14.00	80
6	payment	2020-08-05	41.00	81
1	payment	2020-10-09	60.00	82
10	interest	2020-06-08	100.00	83
4	payment	2020-09-12	16.00	84
4	payment	2020-03-17	5.00	85
10	payment	2020-01-14	20.00	86
5	fee	2020-01-26	28.00	87
5	interest	2020-08-22	61.00	88
3	fee	2020-08-31	91.00	89
3	fee	2020-12-02	96.00	90
5	payment	2020-03-21	91.00	91
9	interest	2020-08-24	72.00	92
9	payment	2020-09-06	58.00	93
2	fee	2020-08-19	61.00	94
5	payment	2020-07-10	7.00	95
6	payment	2020-07-22	18.00	96
5	payment	2020-06-14	19.00	97
7	fee	2020-05-08	84.00	98
4	interest	2020-03-27	84.00	99
4	fee	2020-01-31	70.00	100
\.


--
-- Data for Name: loans; Type: TABLE DATA; Schema: public; Owner: poggers
--

COPY public.loans (loan_id, start_date, initial_amt) FROM stdin;
1	2019-12-17	362.00
2	2019-12-07	483.00
3	2019-12-15	282.00
4	2019-12-27	150.00
5	2019-12-31	219.00
6	2019-12-25	369.00
7	2019-12-16	200.00
8	2019-12-15	65.00
9	2019-12-08	393.00
10	2019-12-05	351.00
\.


--
-- Data for Name: ttest; Type: TABLE DATA; Schema: public; Owner: poggers
--

COPY public.ttest (id, value) FROM stdin;
1	1
2	45
3	72
\.


--
-- Name: loan_events_tx_id_seq; Type: SEQUENCE SET; Schema: public; Owner: poggers
--

SELECT pg_catalog.setval('public.loan_events_tx_id_seq', 100, true);


--
-- Name: loans_loan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: poggers
--

SELECT pg_catalog.setval('public.loans_loan_id_seq', 1, false);


--
-- Name: ttest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: poggers
--

SELECT pg_catalog.setval('public.ttest_id_seq', 3, true);


--
-- Name: loan_events loan_events_pkey; Type: CONSTRAINT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.loan_events
    ADD CONSTRAINT loan_events_pkey PRIMARY KEY (tx_id);


--
-- Name: loans loans_pkey; Type: CONSTRAINT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_pkey PRIMARY KEY (loan_id);


--
-- Name: ttest ttest_pkey; Type: CONSTRAINT; Schema: public; Owner: poggers
--

ALTER TABLE ONLY public.ttest
    ADD CONSTRAINT ttest_pkey PRIMARY KEY (id);


--
-- Name: ix_loaninfo_loans_index; Type: INDEX; Schema: loaninfo; Owner: poggers
--

CREATE INDEX ix_loaninfo_loans_index ON loaninfo.loans USING btree (index);


--
-- PostgreSQL database dump complete
--

