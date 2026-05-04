def generate_dockerfile(input_data, use_ai=True):
    
    # ❌ If AI not selected → FAIL
    if not use_ai:
        return None

    try:
        data = input_data.lower()

        # ---------------- PYTHON ----------------
        if "python" in data:
            return """FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]"""

        # ---------------- NODE ----------------
        elif "node" in data:
            return """FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]"""

        # ---------------- JAVA ----------------
        elif "java" in data:
            return """FROM openjdk:17
WORKDIR /app
COPY . .
CMD ["java", "-jar", "app.jar"]"""

        else:
            return None

    except:
        return None