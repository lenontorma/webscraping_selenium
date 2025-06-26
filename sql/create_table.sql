CREATE TABLE imoveis (
    id SERIAL PRIMARY KEY,
    card INTEGER,
    url TEXT,
    endereco TEXT,
    tipo_imovel TEXT,
    aluguel NUMERIC,
    condominio NUMERIC,
    iptu NUMERIC,
    total NUMERIC
);
