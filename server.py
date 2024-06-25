import http.server
import socketserver
import os
import json
import random
from datetime import datetime

# Load resume data from JSON file
with open('resume.json') as f:
    resume_data = json.load(f)

# Get the PORT environment variable, with a fallback to 8000 for local testing
PORT = int(os.environ.get('PORT', 8000))

class ChatbotHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Send response to preflight requests
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data.decode('utf-8'))

        user_input = request_data.get('message')
        response = self.generate_response(user_input)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.end_headers()
        self.wfile.write(json.dumps({'response': response}).encode('utf-8'))

    def generate_response(self, user_input):
        # Simple keyword-based response generation
        if 'education' in user_input.lower() or 'study' in user_input.lower() or 'degree' in user_input.lower()or 'qualification' in user_input.lower():
            return self.format_education(resume_data['education'])
        
        elif 'experience' in user_input.lower() or 'work' in user_input.lower():
            return self.format_experience(resume_data['experience'])
        
        elif 'hi' in user_input.lower() or 'hey' in user_input.lower() or 'hello' in user_input.lower() or 'bujji' in user_input.lower():
            return random.choice(resume_data['greetings'])
        
        elif 'contact' in user_input.lower() or 'mail' in user_input.lower() or 'social' in user_input.lower():
            return random.choice(resume_data['contact_info'])
        
        elif 'about me' in user_input.lower() or 'about him' in user_input.lower() or 'about yourself' in user_input.lower():
            return random.choice(resume_data['about_me'])
        
        elif 'skills' in user_input.lower():
            return self.format_skills(resume_data['skills'])
        
        elif 'certifications' in user_input.lower() or 'certification' in user_input.lower():
            return self.format_certifications(resume_data['certifications'])

        elif 'projects' in user_input.lower():
            return self.format_projects(resume_data['projects'])
        
        elif 'summary' in user_input.lower():
            return self.format_summary(resume_data['summary'])
        
        elif 'accomplishments' in user_input.lower() or 'achievement' in user_input.lower() or 'accomplishment' in user_input.lower():
            return self.format_accomp(resume_data['accomplishments'])
        
        elif 'hobbies' in user_input.lower():
            return self.format_hobbies(resume_data['hobbies'])
        
        elif 'free time' in user_input.lower() or 'what do you do in your free time' in user_input.lower():
            return random.choice(resume_data['free_time_activities'])
        
        elif 'time' in user_input.lower():
            return resume_data['additional_info']['current_time'] + datetime.now().strftime("%H:%M:%S")

        elif 'favorite food' in user_input.lower():
            return resume_data['additional_info']['favorite_food']

        elif 'favorite place' in user_input.lower():
            return resume_data['additional_info']['favorite_place']

        elif 'favorite color' in user_input.lower():
            return resume_data['additional_info']['favorite_color']
        
        else:
            return random.choice(resume_data['fallback'])

    def format_education(self, education):
        return "<br>".join([f"{edu['degree']} from {edu['institution']} ({edu['period']})" for edu in education])

    def format_experience(self, experience):
        return "<br>".join([f"{exp['title']} at {exp['company']} ({exp['period']})" for exp in experience])

    def format_skills(self, skills):
        return "<br>".join(skills)
    
    def format_certifications(self, certifications):
        return "<br>".join(certifications)
    
    def format_accomp(self, accomplishments):
        return "<br>".join(accomplishments)
    
    def format_summary(self, summary):
        return summary
    
    def format_hobbies(self, hobbies):
        return "<br>" .join(hobbies)
    
    def format_projects(self, projects):
        return "<br>".join([f"{proj['title']} ({proj['period']})" for proj in projects])

Handler = ChatbotHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()