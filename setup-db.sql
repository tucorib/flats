CREATE TABLE public.source
(
  id integer NOT NULL DEFAULT nextval('source_seq'::regclass),
  name character varying(255),
  CONSTRAINT source_pk PRIMARY KEY (id),
  CONSTRAINT source_name_un UNIQUE (name)
);
CREATE SEQUENCE public.source_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 4
  CACHE 1;

CREATE TABLE public.flat
(
  id integer NOT NULL DEFAULT nextval('flat_seq'::regclass),
  source_id integer NOT NULL,
  reference character varying(255),
  url text NOT NULL,
  date timestamp with time zone NOT NULL,
  CONSTRAINT flat_pk PRIMARY KEY (id),
  CONSTRAINT flat_source_id FOREIGN KEY (source_id)
      REFERENCES public.source (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT flat_reference_un UNIQUE (source_id, reference)
);
CREATE SEQUENCE public.flat_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
CREATE INDEX fki_flat_source_id
  ON public.flat
  USING btree
  (source_id);
