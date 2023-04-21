from uuid import UUID

from app import ModelMixin
from settings import Config

path = 'igor/baohule/config/prisma-config/prisma/prisma/casino-prisma.prisma'
import os
from sqlalchemy import create_engine, inspect, UniqueConstraint

# Define a mapping of SQLAlchemy types to Prisma types
type_mapping = {
    # SQLAlchemy types
    'Integer': 'Int',
    'BigInteger': 'BigInt',
    'SmallInteger': 'Int',
    'Float': 'Float',
    'Numeric': 'Decimal',
    'Boolean': 'Boolean',
    'Date': 'DateTime',
    'Time': 'DateTime',
    'DateTime': 'DateTime',
    'Interval': 'Int',
    'String': 'String',
    'Text': 'String',
    'Unicode': 'String',
    'UnicodeText': 'String',
    'JSON': 'Json',
    'ARRAY': 'Json',  # Map PostgreSQL ARRAY to Json in Prisma
    'UUID': 'String',  # Map UUID to String in Prisma

    # PostgreSQL specific types
    'BIT': 'String',
    'VARBIT': 'String',
    'BYTEA': 'Bytes',
    'CIDR': 'String',
    'INET': 'String',
    'MACADDR': 'String',
    'JSONB': 'Json',
    'TSVECTOR': 'String',
    'TSQUERY': 'String',
    'INT4RANGE': 'String',
    'INT8RANGE': 'String',
    'NUMRANGE': 'String',
    'TSRANGE': 'String',
    'TSTZRANGE': 'String',
}
from sqlalchemy import inspect
from sqlalchemy.orm import RelationshipProperty
from typing import Any, Dict, List


def prisma_generator(model: Any, schema_name: str) -> str:
    metadata = model.metadata
    inspector = inspect(metadata.bind)
    table_names = inspector.get_table_names(schema=schema_name)

    prisma = ""
    for table_name in table_names:
        table = metadata.tables[table_name]
        prisma += f"model {table_name} {{\n"
        columns = table.columns
        for column in columns:
            column_name = column.name
            column_type = column.type
            prisma += f"    {column_name} "
            if isinstance(column_type, RelationshipProperty):
                target_table = column_type.mapper.class_.__tablename__
                prisma += f"{target_table}"
            elif str(column_type) in type_mapping:
                prisma += f"{type_mapping[str(column_type)]}"
            else:
                prisma += f"{str(column_type)}"
            if not column.nullable:
                prisma += " @required"
            if column.primary_key:
                prisma += " @id"
            if column.unique:
                prisma += " @unique"
            prisma += "\n"

        constraints = table.constraints
        for constraint in constraints:
            if isinstance(constraint, UniqueConstraint):
                columns = constraint.columns
                if len(columns) > 1:
                    columns = "{" + ", ".join([str(col.name) for col in columns]) + "}"
                else:
                    columns = str(columns[0].name)
                prisma += f"    @@unique([{columns}])\n"

        indexes = table.indexes
        for index in indexes:
            if not index.unique:
                columns = index.columns
                if len(columns) > 1:
                    columns = "{" + ", ".join([str(col.name) for col in columns]) + "}"
                else:
                    columns = str(columns[0].name)
                prisma += f"    @@index([{columns}])\n"

        for column in columns:
            column_type = column.type
            if str(column_type).startswith("ENUM"):
                enum_values = str(column_type)[5:-1].split(",")
                prisma += f"    {column_name}_enum: Enum {{" + ", ".join([f"{ev.strip()}" for ev in enum_values]) + "}}\n"

        relationships = table.foreign_keys
        for relationship in relationships:
            local_column = relationship.parent
            foreign_column = relationship.column
            target_table = foreign_column.table.name
            target_column = foreign_column.name
            prisma += f"    {local_column.name}: {target_table}@relation(fields: [{local_column.name}], references: [{target_column}])\n"

        prisma += "}\n\n"

    return prisma


def is_valid_type(sqlalchemy_type):
    """
    Check if a given SQLAlchemy type can be mapped to a valid Prisma type.
    """
    valid_types = ['String', 'Int', 'Float', 'Boolean', 'DateTime', 'Json']
    return sqlalchemy_type.__class__.__name__ in valid_types


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(f'postgresql+psycopg2://{Config.postgres_connection}')
    Session = sessionmaker(bind=engine)
    session = Session()

    ModelMixin.metadata.reflect(engine)
    prisma = ""
    print(ModelMixin)
    for model in ModelMixin.metadata.tables:
        prisma.join(prisma_generator(model.__class__, "public"))
    # with open(path, 'w') as f:
        #f.write(prisma)
    print(prisma)
