import csv 
import sys  # To exit the program in case of an error

def read_student_data(filename):
    """
    Reads student data from a CSV file.
    
    Args:
    filename (str): Name of the CSV file.

    Returns:
    list: A list containing students' names and their grades.
    """
    data = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the first row as headers

            for row in csv_reader:
                # Skip rows with missing data
                if len(row) < 6:
                    print(f"Missing data: {row}")
                    continue
                try:
                    # Convert grades to integers
                    data.append({
                        'name': row[0],
                        'cyber_security': int(row[1]),
                        'data_science': int(row[2]),
                        'computing_foundation': int(row[3]),
                        'digital_literacy': int(row[4]),
                        'software_foundation': int(row[5])
                    })
                except ValueError:
                    print(f"Invalid data: {row}. Grades must be integers!")
                    sys.exit(1)  # Exit the program on error

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    
    return data

def calculate_average(student):
    """
    Calculates a student's grade average.

    Args:
    student (dict): Dictionary containing student information.

    Returns:
    float: The student's grade average.
    """
    try:
        total = (student['cyber_security'] + student['data_science'] + student['computing_foundation'] + 
                 student['digital_literacy'] + student['software_foundation'])
        average = total / (len(student)-1)  # Average of the lessons
        return round(average, 2)  # Round the average to 2 decimal places
    except KeyError as e:
        print(f"Missing data: {e}")
        return None

def assign_grade(score):
    """
    Assigns a letter grade based on the student's average score.

    Args:
    score (float): The student's average grade.

    Returns:
    str: Letter grade (A, B, C, D, E, F).
    """
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"   

def calculate_min_max_range(student_scores):    
    """
    Calculates the minimum, maximum, and range of a student's grades.

    Args:
    student_scores (list): List of a student's grades in all subjects.

    Returns:
    tuple: (min, max, range) values.
    """
    min_score = min(student_scores)
    max_score = max(student_scores)
    score_range = max_score - min_score
    return min_score, max_score, score_range

def process_student_results(students_data):
    """
    Processes student data, calculates average, letter grade, and statistics.

    Args:
    students_data (list): List containing student information.

    Returns:
    list: List containing processed student results.
    """
    results = []

    for student in students_data:
        student_scores = [student['cyber_security'], student['data_science'], student['computing_foundation'], 
                          student['digital_literacy'], student['software_foundation']]
       
        # Calculate average
        average = calculate_average(student)
        if average is not None:
            grade = assign_grade(average)
           
            # Calculate min, max, and range
            min_score, max_score, score_range = calculate_min_max_range(student_scores)
           
            # Pass or fail?
            pass_fail = "Congratulations, you passed!" if average >= 40 else "Fail"
           
            # Store student results
            student_results = {
                'name': student['name'],
                'cyber_security': student['cyber_security'],
                'data_science': student['data_science'],
                'computing_foundation': student['computing_foundation'],
                'digital_literacy': student['digital_literacy'],
                'software_foundation': student['software_foundation'],
                'average': average,
                'grade': grade,
                'min_score': min_score,
                'max_score': max_score,
                'score_range': score_range,
                'pass_fail': pass_fail
            }
            results.append(student_results)
   
    return results

def write_results_to_csv(results, filename):
    """
    Writes processed student results to a CSV file.

    Args:
    results (list): List containing processed student results.
    filename (str): Name of the output file.
    """
    if results:
        # Define CSV headers
        header = ['name', 'cyber_security', 'data_science', 'computing_foundation', 'digital_literacy', 
                  'software_foundation', 'average', 'grade', 'min_score', 'max_score', 'score_range', 'pass_fail']
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()  # Write header row
            writer.writerows(results)  # Write student results

        print(f"Results written to {filename}!")
    else:
        print("No data to write.")

if __name__ == "__main__":
    # Name of the file containing student data
    filename = "students.csv"

    # Read student data
    students_data = read_student_data(filename)

    if students_data:
        # Process data
        results = process_student_results(students_data)
        # Write results to CSV file
        write_results_to_csv(results, "student_results.csv")

    print("Processing completed. Exiting...")
