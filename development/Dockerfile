FROM public.ecr.aws/lambda/python:3.12

# Copy requirements (if present)
COPY lambda/lambda_ingestion/requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy lambda handler code
COPY lambda/lambda_ingestion/lambda_function.py ${LAMBDA_TASK_ROOT}/

# Copy shared src directory
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set handler
# Format: <file>.<function>
CMD ["lambda_function.lambda_handler"]