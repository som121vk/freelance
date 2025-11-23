"""
PROJECT MANAGEMENT TOOL
FlexWork Agency - Simple Project Tracker
"""

import json
import datetime
from pathlib import Path

class ProjectManager:
    def __init__(self, data_file='projects_data.json'):
        self.data_file = Path(data_file)
        self.projects = self.load_projects()
        
    def load_projects(self):
        """Load projects from JSON file"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_projects(self):
        """Save projects to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.projects, f, indent=2)
    
    def add_project(self, project_data):
        """Add a new project"""
        project = {
            'id': len(self.projects) + 1,
            'client_name': project_data['client_name'],
            'client_email': project_data['client_email'],
            'client_phone': project_data.get('client_phone', ''),
            'project_name': project_data['project_name'],
            'service_type': project_data['service_type'],
            'description': project_data['description'],
            'budget': project_data['budget'],
            'freelancer_share': project_data.get('freelancer_share', 0.60),
            'assigned_to': project_data.get('assigned_to', None),
            'status': 'New',
            'progress': 0,
            'start_date': project_data.get('start_date', str(datetime.date.today())),
            'deadline': project_data['deadline'],
            'created_at': str(datetime.datetime.now()),
            'milestones': [],
            'notes': []
        }
        self.projects.append(project)
        self.save_projects()
        return project
    
    def assign_freelancer(self, project_id, freelancer_name, freelancer_email):
        """Assign a freelancer to a project"""
        project = self.get_project(project_id)
        if project:
            project['assigned_to'] = {
                'name': freelancer_name,
                'email': freelancer_email,
                'assigned_date': str(datetime.date.today())
            }
            project['status'] = 'Assigned'
            self.save_projects()
            return True
        return False
    
    def update_status(self, project_id, status, progress=None):
        """Update project status"""
        valid_statuses = ['New', 'Assigned', 'In Progress', 'In Review', 'Completed', 'On Hold']
        project = self.get_project(project_id)
        
        if project and status in valid_statuses:
            project['status'] = status
            if progress is not None:
                project['progress'] = progress
            self.save_projects()
            return True
        return False
    
    def add_milestone(self, project_id, milestone_name, due_date):
        """Add a milestone to project"""
        project = self.get_project(project_id)
        if project:
            milestone = {
                'name': milestone_name,
                'due_date': due_date,
                'completed': False,
                'completed_date': None
            }
            project['milestones'].append(milestone)
            self.save_projects()
            return True
        return False
    
    def complete_milestone(self, project_id, milestone_index):
        """Mark a milestone as complete"""
        project = self.get_project(project_id)
        if project and milestone_index < len(project['milestones']):
            project['milestones'][milestone_index]['completed'] = True
            project['milestones'][milestone_index]['completed_date'] = str(datetime.date.today())
            self.save_projects()
            return True
        return False
    
    def add_note(self, project_id, note_text):
        """Add a note to project"""
        project = self.get_project(project_id)
        if project:
            note = {
                'text': note_text,
                'timestamp': str(datetime.datetime.now()),
                'author': 'Admin'
            }
            project['notes'].append(note)
            self.save_projects()
            return True
        return False
    
    def get_project(self, project_id):
        """Get a specific project by ID"""
        for project in self.projects:
            if project['id'] == project_id:
                return project
        return None
    
    def get_all_projects(self):
        """Get all projects"""
        return self.projects
    
    def get_projects_by_status(self, status):
        """Filter projects by status"""
        return [p for p in self.projects if p['status'] == status]
    
    def get_active_projects(self):
        """Get all active projects"""
        return [p for p in self.projects if p['status'] in ['Assigned', 'In Progress', 'In Review']]
    
    def calculate_financials(self, project_id):
        """Calculate project financials"""
        project = self.get_project(project_id)
        if not project:
            return None
            
        total = project['budget']
        freelancer_share_percent = project['freelancer_share']
        freelancer_payment = total * freelancer_share_percent
        company_margin = total - freelancer_payment
        
        return {
            'total_budget': total,
            'freelancer_payment': freelancer_payment,
            'company_margin': company_margin,
            'margin_percent': (company_margin / total) * 100
        }
    
    def get_dashboard_stats(self):
        """Get overview statistics"""
        total_projects = len(self.projects)
        active = len(self.get_active_projects())
        completed = len(self.get_projects_by_status('Completed'))
        
        total_revenue = sum(p['budget'] for p in self.projects)
        completed_revenue = sum(p['budget'] for p in self.projects if p['status'] == 'Completed')
        
        return {
            'total_projects': total_projects,
            'active_projects': active,
            'completed_projects': completed,
            'total_revenue': total_revenue,
            'completed_revenue': completed_revenue,
            'pending_revenue': total_revenue - completed_revenue
        }
    
    def generate_report(self):
        """Generate a text report"""
        stats = self.get_dashboard_stats()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           FLEXWORK AGENCY - PROJECT REPORT                   ║
╚══════════════════════════════════════════════════════════════╝

📊 OVERVIEW STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Projects:        {stats['total_projects']}
Active Projects:       {stats['active_projects']}
Completed Projects:    {stats['completed_projects']}

💰 FINANCIAL SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Revenue:         ₹{stats['total_revenue']:,.2f}
Completed Revenue:     ₹{stats['completed_revenue']:,.2f}
Pending Revenue:       ₹{stats['pending_revenue']:,.2f}

📁 ACTIVE PROJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for project in self.get_active_projects():
            assigned = project.get('assigned_to', {})
            freelancer = assigned.get('name', 'Not Assigned') if assigned else 'Not Assigned'
            
            report += f"""
Project #{project['id']}: {project['project_name']}
  Client: {project['client_name']}
  Service: {project['service_type']}
  Status: {project['status']}
  Progress: {project['progress']}%
  Freelancer: {freelancer}
  Budget: ₹{project['budget']:,.2f}
  Deadline: {project['deadline']}
"""
        
        report += "\n" + "═" * 64 + "\n"
        return report


# CLI Interface
def main():
    pm = ProjectManager()
    
    while True:
        print("\n" + "="*60)
        print("🚀 FLEXWORK AGENCY - PROJECT MANAGEMENT SYSTEM")
        print("="*60)
        print("\n📋 MAIN MENU:")
        print("1. 📊 View Dashboard")
        print("2. ➕ Add New Project")
        print("3. 👥 Assign Freelancer")
        print("4. 📈 Update Project Status")
        print("5. 📁 View All Projects")
        print("6. 💰 View Project Financials")
        print("7. 📝 Add Note to Project")
        print("8. 📄 Generate Report")
        print("9. 🚪 Exit")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            # Dashboard
            stats = pm.get_dashboard_stats()
            print("\n" + "="*60)
            print("📊 DASHBOARD OVERVIEW")
            print("="*60)
            print(f"Total Projects: {stats['total_projects']}")
            print(f"Active Projects: {stats['active_projects']}")
            print(f"Completed Projects: {stats['completed_projects']}")
            print(f"\n💰 Total Revenue: ₹{stats['total_revenue']:,.2f}")
            print(f"💰 Completed Revenue: ₹{stats['completed_revenue']:,.2f}")
            print(f"💰 Pending Revenue: ₹{stats['pending_revenue']:,.2f}")
            
        elif choice == '2':
            # Add Project
            print("\n" + "="*60)
            print("➕ ADD NEW PROJECT")
            print("="*60)
            
            project_data = {
                'client_name': input("Client Name: ").strip(),
                'client_email': input("Client Email: ").strip(),
                'client_phone': input("Client Phone: ").strip(),
                'project_name': input("Project Name: ").strip(),
                'service_type': input("Service Type (Web/Design/App/Video/Content/Marketing): ").strip(),
                'description': input("Project Description: ").strip(),
                'budget': float(input("Budget (₹): ").strip()),
                'deadline': input("Deadline (YYYY-MM-DD): ").strip()
            }
            
            project = pm.add_project(project_data)
            print(f"\n✅ Project #{project['id']} created successfully!")
            
        elif choice == '3':
            # Assign Freelancer
            project_id = int(input("\nEnter Project ID: ").strip())
            freelancer_name = input("Freelancer Name: ").strip()
            freelancer_email = input("Freelancer Email: ").strip()
            
            if pm.assign_freelancer(project_id, freelancer_name, freelancer_email):
                print(f"\n✅ Freelancer assigned successfully!")
            else:
                print(f"\n❌ Project not found!")
                
        elif choice == '4':
            # Update Status
            project_id = int(input("\nEnter Project ID: ").strip())
            print("\nStatuses: New, Assigned, In Progress, In Review, Completed, On Hold")
            status = input("New Status: ").strip()
            progress = input("Progress (0-100, or leave blank): ").strip()
            progress = int(progress) if progress else None
            
            if pm.update_status(project_id, status, progress):
                print(f"\n✅ Status updated successfully!")
            else:
                print(f"\n❌ Failed to update status!")
                
        elif choice == '5':
            # View All Projects
            print("\n" + "="*60)
            print("📁 ALL PROJECTS")
            print("="*60)
            
            for project in pm.get_all_projects():
                print(f"\n#{project['id']} - {project['project_name']}")
                print(f"  Client: {project['client_name']}")
                print(f"  Service: {project['service_type']}")
                print(f"  Status: {project['status']} ({project['progress']}%)")
                print(f"  Budget: ₹{project['budget']:,.2f}")
                print(f"  Deadline: {project['deadline']}")
                
        elif choice == '6':
            # Financials
            project_id = int(input("\nEnter Project ID: ").strip())
            financials = pm.calculate_financials(project_id)
            
            if financials:
                print("\n" + "="*60)
                print("💰 PROJECT FINANCIALS")
                print("="*60)
                print(f"Total Budget: ₹{financials['total_budget']:,.2f}")
                print(f"Freelancer Payment: ₹{financials['freelancer_payment']:,.2f}")
                print(f"Company Margin: ₹{financials['company_margin']:,.2f}")
                print(f"Margin %: {financials['margin_percent']:.2f}%")
            else:
                print("\n❌ Project not found!")
                
        elif choice == '7':
            # Add Note
            project_id = int(input("\nEnter Project ID: ").strip())
            note = input("Note: ").strip()
            
            if pm.add_note(project_id, note):
                print(f"\n✅ Note added successfully!")
            else:
                print(f"\n❌ Project not found!")
                
        elif choice == '8':
            # Generate Report
            print(pm.generate_report())
            
            # Ask to save
            save = input("\nSave report to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"report_{datetime.date.today()}.txt"
                with open(filename, 'w') as f:
                    f.write(pm.generate_report())
                print(f"\n✅ Report saved to {filename}")
                
        elif choice == '9':
            print("\n👋 Thank you for using FlexWork Project Manager!")
            break
            
        else:
            print("\n❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
