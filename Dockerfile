FROM python:3.11-slim

WORKDIR /app


# Install OS dependencies
RUN apt-get update && apt-get install -y build-essential


COPY . .

# Install build tools and your package
RUN pip install --upgrade pip setuptools wheel
RUN pip install 


# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app via uvicorn
CMD ["uvicorn", "hungsql.server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]