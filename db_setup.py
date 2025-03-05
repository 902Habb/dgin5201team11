# db_setup.py

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create a base class for our models
Base = declarative_base()

# Define our database models
class COMBCategory(Base):
    """
    Represents the 6 COM-B categories:
    - Capability - Physical
    - Capability - Psychological
    - Opportunity - Social
    - Opportunity - Physical
    - Motivation - Automatic
    - Motivation - Reflective
    """
    __tablename__ = 'comb_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    
    # Establish relationships with other tables
    indicators = relationship("Indicator", back_populates="category")
    examples = relationship("CodingExample", back_populates="category")
    results = relationship("AnalysisResult", back_populates="category")

class Indicator(Base):
    """
    Indicators help identify when text belongs to a certain COM-B category.
    They can be positive (suggesting inclusion) or negative (suggesting exclusion).
    """
    __tablename__ = 'indicators'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('comb_categories.id'), nullable=False)
    text = Column(Text, nullable=False)
    indicator_type = Column(String(10), nullable=False)  # 'positive' or 'negative'
    
    # Establish relationship with category
    category = relationship("COMBCategory", back_populates="indicators")

class CodingExample(Base):
    """
    Examples of coded text to guide the AI in its coding decisions.
    """
    __tablename__ = 'coding_examples'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('comb_categories.id'), nullable=False)
    text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)  # Optional explanation of why this text fits the category
    
    # Establish relationship with category
    category = relationship("COMBCategory", back_populates="examples")

class AnalysisResult(Base):
    """
    Stores the results of AI analysis on transcript text.
    """
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True)
    text_quote = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('comb_categories.id'), nullable=False)
    confidence = Column(Float, nullable=False)
    session_id = Column(String(100), nullable=False)  # To group results from the same analysis session
    
    # Establish relationship with category
    category = relationship("COMBCategory", back_populates="results")

# Create the database
def setup_database():
    # Create a SQLite database file in the current directory
    engine = create_engine('sqlite:///comb_analyzer.db')
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    
    return Session()

if __name__ == "__main__":
    # Set up the database when this script is run directly
    session = setup_database()
    print("Database created successfully!")