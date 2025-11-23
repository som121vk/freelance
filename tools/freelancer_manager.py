"""
FREELANCER MANAGEMENT TOOL
FlexWork Agency - Manage Freelancer Network
"""

import json
from pathlib import Path
from datetime import datetime

class FreelancerManager:
    def __init__(self, data_file='freelancers_data.json'):
        self.data_file = Path(data_file)
        self.freelancers = self.load_freelancers()
    
    def load_freelancers(self):
        """Load freelancers from JSON"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_freelancers(self):
        """Save freelancers to JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.freelancers, f, indent=2)
    
    def add_freelancer(self, freelancer_data):
        """Add new freelancer"""
        freelancer = {
            'id': len(self.freelancers) + 1,
            'name': freelancer_data['name'],
            'email': freelancer_data['email'],
            'phone': freelancer_data['phone'],
            'skills': freelancer_data['skills'],  # List
            'experience_years': freelancer_data['experience_years'],
            'hourly_rate': freelancer_data.get('hourly_rate', 500),
            'revenue_share': freelancer_data.get('revenue_share', 0.60),
            'portfolio_link': freelancer_data.get('portfolio_link', ''),
            'rating': 0,
            'projects_completed': 0,
            'total_earned': 0,
            'status': 'Active',
            'joined_date': str(datetime.now().date()),
            'payment_method': freelancer_data.get('payment_method', 'Bank Transfer'),
            'bank_details': freelancer_data.get('bank_details', {}),
            'notes': []
        }
        self.freelancers.append(freelancer)
        self.save_freelancers()
        return freelancer
    
    def get_freelancer(self, freelancer_id):
        """Get freelancer by ID"""
        for f in self.freelancers:
            if f['id'] == freelancer_id:
                return f
        return None
    
    def search_by_skill(self, skill):
        """Find freelancers with specific skill"""
        return [f for f in self.freelancers if skill.lower() in [s.lower() for s in f['skills']]]
    
    def update_rating(self, freelancer_id, new_rating):
        """Update freelancer rating (1-5)"""
        freelancer = self.get_freelancer(freelancer_id)
        if freelancer and 1 <= new_rating <= 5:
            # Calculate average if there are previous ratings
            current_rating = freelancer['rating']
            projects = freelancer['projects_completed']
            
            if projects == 0:
                freelancer['rating'] = new_rating
            else:
                total_rating = current_rating * projects + new_rating
                freelancer['rating'] = total_rating / (projects + 1)
            
            self.save_freelancers()
            return True
        return False
    
    def complete_project(self, freelancer_id, payment_amount):
        """Mark project as completed and update stats"""
        freelancer = self.get_freelancer(freelancer_id)
        if freelancer:
            freelancer['projects_completed'] += 1
            freelancer['total_earned'] += payment_amount
            self.save_freelancers()
            return True
        return False
    
    def get_top_performers(self, limit=5):
        """Get top performing freelancers"""
        sorted_freelancers = sorted(
            self.freelancers,
            key=lambda f: (f['rating'], f['projects_completed']),
            reverse=True
        )
        return sorted_freelancers[:limit]
    
    def generate_freelancer_report(self):
        """Generate freelancer performance report"""
        total = len(self.freelancers)
        active = len([f for f in self.freelancers if f['status'] == 'Active'])
        total_projects = sum(f['projects_completed'] for f in self.freelancers)
        total_paid = sum(f['total_earned'] for f in self.freelancers)
        avg_rating = sum(f['rating'] for f in self.freelancers if f['rating'] > 0) / max(len([f for f in self.freelancers if f['rating'] > 0]), 1)
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║         FLEXWORK AGENCY - FREELANCER REPORT                  ║
╚══════════════════════════════════════════════════════════════╝

👥 FREELANCER STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Freelancers:     {total}
Active Freelancers:    {active}
Total Projects:        {total_projects}
Average Rating:        {avg_rating:.2f} ⭐

💰 FINANCIAL SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Paid Out:        ₹{total_paid:,.2f}

🏆 TOP PERFORMERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for idx, f in enumerate(self.get_top_performers(5), 1):
            report += f"""
{idx}. {f['name']}
   Rating: {f['rating']:.1f}⭐ | Projects: {f['projects_completed']} | Earned: ₹{f['total_earned']:,.2f}
   Skills: {', '.join(f['skills'][:3])}
"""
        
        return report


def main():
    fm = FreelancerManager()
    
    while True:
        print("\n" + "="*60)
        print("👥 FLEXWORK AGENCY - FREELANCER MANAGEMENT")
        print("="*60)
        print("\n📋 MENU:")
        print("1. ➕ Add New Freelancer")
        print("2. 👀 View All Freelancers")
        print("3. 🔍 Search by Skill")
        print("4. ⭐ Update Rating")
        print("5. ✅ Mark Project Complete")
        print("6. 🏆 View Top Performers")
        print("7. 📄 Generate Report")
        print("8. 🚪 Exit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == '1':
            print("\n" + "="*60)
            print("➕ ADD NEW FREELANCER")
            print("="*60)
            
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            skills = input("Skills (comma-separated): ").strip().split(',')
            skills = [s.strip() for s in skills]
            exp = int(input("Years of Experience: ").strip())
            hourly = float(input("Hourly Rate (₹): ").strip())
            share = float(input("Revenue Share (0.xx, e.g., 0.60 for 60%): ").strip())
            portfolio = input("Portfolio Link (optional): ").strip()
            
            freelancer_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience_years': exp,
                'hourly_rate': hourly,
                'revenue_share': share,
                'portfolio_link': portfolio
            }
            
            freelancer = fm.add_freelancer(freelancer_data)
            print(f"\n✅ Freelancer #{freelancer['id']} added successfully!")
            
        elif choice == '2':
            print("\n" + "="*60)
            print("👥 ALL FREELANCERS")
            print("="*60)
            
            for f in fm.freelancers:
                print(f"\n#{f['id']} - {f['name']}")
                print(f"  📧 {f['email']} | 📱 {f['phone']}")
                print(f"  💼 Skills: {', '.join(f['skills'])}")
                print(f"  ⭐ Rating: {f['rating']:.1f} | Projects: {f['projects_completed']}")
                print(f"  💰 Earned: ₹{f['total_earned']:,.2f}")
                print(f"  Status: {f['status']}")
                
        elif choice == '3':
            skill = input("\nEnter skill to search: ").strip()
            results = fm.search_by_skill(skill)
            
            if results:
                print(f"\n✅ Found {len(results)} freelancer(s) with '{skill}':")
                for f in results:
                    print(f"  #{f['id']} - {f['name']} (Rating: {f['rating']:.1f}⭐)")
            else:
                print(f"\n❌ No freelancers found with skill '{skill}'")
                
        elif choice == '4':
            fid = int(input("\nFreelancer ID: ").strip())
            rating = float(input("New Rating (1-5): ").strip())
            
            if fm.update_rating(fid, rating):
                print(f"\n✅ Rating updated!")
            else:
                print(f"\n❌ Failed to update rating!")
                
        elif choice == '5':
            fid = int(input("\nFreelancer ID: ").strip())
            amount = float(input("Payment Amount (₹): ").strip())
            
            if fm.complete_project(fid, amount):
                print(f"\n✅ Project marked complete!")
            else:
                print(f"\n❌ Freelancer not found!")
                
        elif choice == '6':
            print("\n" + "="*60)
            print("🏆 TOP PERFORMERS")
            print("="*60)
            
            for idx, f in enumerate(fm.get_top_performers(), 1):
                print(f"\n{idx}. {f['name']}")
                print(f"   Rating: {f['rating']:.1f}⭐")
                print(f"   Projects: {f['projects_completed']}")
                print(f"   Total Earned: ₹{f['total_earned']:,.2f}")
                
        elif choice == '7':
            print(fm.generate_freelancer_report())
            
            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"freelancer_report_{datetime.now().date()}.txt"
                with open(filename, 'w') as file:
                    file.write(fm.generate_freelancer_report())
                print(f"\n✅ Saved to {filename}")
                
        elif choice == '8':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice!")


if __name__ == "__main__":
    main()
