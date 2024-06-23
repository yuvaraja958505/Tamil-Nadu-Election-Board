import mysql.connector
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient, subject, body):

    sender_email = "Enter_your_email@gmail.com"
    sender_password = "Enter_your_password"  # Consider using environment variables for security.
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Replace with your SMTP server details.
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def candidate():
    candidates = {
        "1": {"name": "Vasu", "party": "DMK"},
        "2": {"name": "M.Shanmugam", "party": "ADMK"},
        "3": {"name": "P.Chidambaram", "party": "INC"},
        "4": {"name": "R.Dharmar", "party": "AIADMK"},
        "5": {"name": "Vaiko", "party": "BJP"}
    }
    
    print("---candidate-name-list---")
    for num, details in candidates.items():
        print(f"no:{num} candidate_name: {details['name']} katchi_name:{details['party']}")
        
    user = input("user enter for you vote:")
    if user in candidates:
        candidate_name = candidates[user]['name']
        party = candidates[user]['party']
        timestamp = datetime.datetime.now()
        
        # Log the vote
        with open("vote.txt", "a") as f:
            log_entry = f"your vote for {party}. candidate name is '{candidate_name}' {timestamp}\n"
            f.write(log_entry)
            print(log_entry)
            f.write("your successfully voted\n")
            print("your successfully voted")
        
        # Update the database
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="election_db"
            )
            mycursor = mydb.cursor()
            update_sql = "UPDATE candidate SET votes = votes + 1 WHERE candidate_id = %s"
            mycursor.execute(update_sql, (user,))
            mydb.commit()
            print("Vote updated in database successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            mycursor.close()
            mydb.close()
        
        # Send email confirmation
        email = input("Enter your email to receive a vote confirmation: ")
        email_body = f"Thank you for voting!\n\nYou voted for {party}.\nCandidate name: {candidate_name}\nTime: {timestamp}"
        send_email(email, "Vote Confirmation", email_body)
        
    else:
        print("Invalid choice. You did not vote.")

candidate()









