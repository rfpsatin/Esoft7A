import uuid
from sqlalchemy import create_engine, Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, FLOAT
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from typing import List
from cluster_analysis import logger

class Base(DeclarativeBase):
    pass

class DbCluster(Base):
    __tablename__ = "clusters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    virtual_centroid_features: Mapped[List[float]] = mapped_column(ARRAY(FLOAT), nullable=False)
    elements: Mapped[List["DbElement"]] = relationship("DbElement", back_populates="cluster", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<DbCluster(id={self.id}, virtual_centroid_features={self.virtual_centroid_features})>"


class DbElement(Base):
    __tablename__ = "elements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    features: Mapped[List[float]] = mapped_column(ARRAY(FLOAT), nullable=False)
    is_centroid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clusters.id"), nullable=False)
    cluster: Mapped["DbCluster"] = relationship("DbCluster", back_populates="elements")

    def __repr__(self) -> str:
        return f"<DbElement(id={self.id}, features={self.features}, is_centroid={self.is_centroid}, cluster_id={self.cluster_id})>"


if __name__ == '__main__':
    DATABASE_URL = "postgresql://user:password@localhost:5432/bitcoin_cluster_db"

    engine = create_engine(DATABASE_URL, echo=True)

    def create_tables():
        Base.metadata.create_all(bind=engine)
        logger.log("Tabelas criadas.")

    create_tables()

    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()

    try:
        features_cluster = [1.0, 2.0]
        novo_cluster = DbCluster(virtual_centroid_features=features_cluster)
        db_session.add(novo_cluster)
        db_session.commit() # Salva o cluster para obter seu ID
        db_session.refresh(novo_cluster)
        logger.log(f"Cluster criado: {novo_cluster}")

        features_elemento = [1.1, 2.1]
        novo_elemento = DbElement(
            features=features_elemento,
            is_centroid=True,
            cluster_id=novo_cluster.id # Associa ao cluster recem criado
        )
        db_session.add(novo_elemento)
        db_session.commit()
        logger.log(f"Elemento criado: {novo_elemento}")

    except Exception as e:
        logger.log(f"Erro durante SGBD: {e}", level="ERROR")
        db_session.rollback()
    finally:
        db_session.close()

    logger.log("Arquivo database_models.py carregado com sucesso.")