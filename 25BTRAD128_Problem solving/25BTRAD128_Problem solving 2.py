# Student grading automation.
# Code: 
def calculate_grade(score):  
  """Returns letter grade and status based on score."""    
  if score >= 90:       
    return "A", "Pass"    
  elif score >= 80:    
    return "B", "Pass"
  elif score >= 70:   
    return "C", "Pass" 
  elif score >= 60:    
    return "D", "Pass"   
  else:     
      return "F", "Fail" 
    
  def main(): 
        print("=== Student Grading Automation System ===")   
        students = []   
    try:       
      num_students = int(input("Enter total number of students: "))      
      for i in range(1, num_students + 1):    
        print(f"\nStudent {i}:")      
        name = input(" Enter name: ").strip()         
        score = float(input(" Enter score (0-100): "))   
        while score < 0 or score > 100:      
          print(" Score must be between 0 and 100.")       
          score = float(input(" Enter score (0-100): "))       
        grade, status = calculate_grade(score)      
        students.append({             
          "name": name,        
          "score": score,     
          "grade": grade,    
          "status": status     
        })                    
        
#Display Results  
      print("\n" + "=" * 45)   
      print(f"{'Name':<15} | {'Score':<8} | {'Grade':<6} | {'Status':<6}")      
      print("=" * 45) 
      total_score = 0     
      for student in students:    
        print(f"{student['name']:<15} | {student['score']:<8.2f} | {student['g rade']:<6} | {student['status']:<6}")            
        total_score += student['score']      
      print("-" * 45)   
      class_average = total_score / num_students if num_students > 0 else 0 
      print(f"Class Average: {class_average:.2f}")       
      print("=" * 45)   
  except ValueError:     
    print("Invalid input! Please enter valid numeric values for counts and scores.")
