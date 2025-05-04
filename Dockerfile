FROM python:3.11-slim

WORKDIR /app

# Copy your code and dependencies
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app via uvicorn
CMD ["uvicorn", "hungsql.server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]