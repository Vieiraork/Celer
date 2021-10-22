-- script do banco

CREATE TABLE "usuario" (
	"id" SERIAL,
	"nome" TEXT,
	"login" TEXT UNIQUE,
	"senha" TEXT,
	"apto" TEXT,
	"tipo_conta" TEXT,
	"usuario_condominio" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("usuario_condominio") REFERENCES "condominio"("id")
);

CREATE TABLE "condominio" (
	"id" SERIAL,
	"nome" TEXT,
	"endereco" TEXT UNIQUE,
	"estado" TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "encomenda" (
	"id" SERIAL,
	"descricao" TEXT,
	"data" DATE,
	"qtd" INTEGER,
	"recebimento_porteiro" TEXT,
	"recebimento_morador" TEXT,
	"encomenda_usuario" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("encomenda_usuario") REFERENCES "usuario"("id")
);
