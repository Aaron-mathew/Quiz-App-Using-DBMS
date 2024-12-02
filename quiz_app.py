import json
import random
import time
from datetime import datetime, timedelta

import mysql.connector 


# Connect to MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='aaron',
            database='quiz_app'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def initialize_database():
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed. Exiting.")
        return
    
    cursor = conn.cursor()
    if conn.is_connected():
        print("Connected to MySQL database")
    else:
        print("Connection failed")
        return
        
    # Ensure tables exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        college VARCHAR(255),
        course VARCHAR(255),
        contact_number VARCHAR(15),
        hints_used INT DEFAULT 0,
        achievements TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        achievement VARCHAR(255),
        FOREIGN KEY (username) REFERENCES users(username)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions ( 
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(255),
        difficulty VARCHAR(255),
        question TEXT,
        options TEXT,
        answer INT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_challenge (
        id INT AUTO_INCREMENT PRIMARY KEY,
        challenge_date DATE,
        questions JSON
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        score INT,
        FOREIGN KEY (username) REFERENCES users(username)
    )""")

    conn.commit()
    populate_questions()
    cursor.close()
    conn.close()

# Populate Questions
def populate_questions():
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed. Cannot populate questions.")
        return
    cursor = conn.cursor()

    sample_questions = {
            "DBMS": {
                "Easy": [
                    {"question": "What does DBMS stand for?", "options": ["Database Management System", "Data Backup Management System", "Database Machine System", "Data Management System"], "answer": 1},
                    {"question": "Which of the following is a DBMS software?", "options": ["MySQL", "Word", "Excel", "PowerPoint"], "answer": 1},
                    {"question": "Which of the following is a data model used in DBMS?", "options": ["Hierarchical", "Network", "Relational", "All of the above"], "answer": 4},
                    {"question": "In DBMS, what is a primary key?", "options": ["A unique identifier for a record", "A key used for sorting", "A foreign key", "A key that is used for backup"], "answer": 1},
                    {"question": "Which of the following is a relational database management system?", "options": ["Oracle", "MS Access", "SQL Server", "All of the above"], "answer": 4},
                    {"question": "Which language is used to interact with a DBMS?", "options": ["SQL", "HTML", "C", "Python"], "answer": 1},
                    {"question": "What is normalization in DBMS?", "options": ["Process of converting data into a more useful format", "Process of organizing data", "Process of back up", "Process of reducing data size"], "answer": 2},
                    {"question": "What is the purpose of a foreign key in DBMS?", "options": ["To link two tables", "To encrypt data", "To create indexes", "To store a backup"], "answer": 1},
                    {"question": "Which of the following is not a part of DBMS?", "options": ["Database", "Query processor", "Printer", "Transaction manager"], "answer": 3},
                    {"question": "Which of the following is a component of a DBMS?", "options": ["DBMS engine", "Database schema", "Database manager", "All of the above"], "answer": 4}
                ],
                "Medium": [
                    {"question": "What is an index in DBMS?", "options": ["A special type of table", "A pointer to data", "A stored procedure", "None of the above"], "answer": 2},
                    {"question": "Which of the following ensures that no data is lost in a transaction?", "options": ["Atomicity", "Consistency", "Isolation", "Durability"], "answer": 1},
                    {"question": "Which is a type of SQL join?", "options": ["Inner join", "Outer join", "Cross join", "All of the above"], "answer": 4},
                    {"question": "What is denormalization?", "options": ["Splitting a table into smaller tables", "Combining tables to optimize performance", "Removing redundant data", "None of the above"], "answer": 2},
                    {"question": "Which of the following is true about a deadlock in DBMS?", "options": ["All processes can proceed after a deadlock", "Deadlock leads to blocking of processes", "It occurs due to excess resources", "It is a form of concurrency control"], "answer": 2},
                    {"question": "What is ACID in DBMS?", "options": ["Atomicity, Consistency, Isolation, Durability", "Access Control Identification", "Application Communication Interface Database", "Automatic Control Information Database"], "answer": 1},
                    {"question": "Which command is used to remove all rows from a table without deleting the table?", "options": ["DELETE", "REMOVE", "TRUNCATE", "DROP"], "answer": 3},
                    {"question": "In a relational database, a table is also known as:", "options": ["Relation", "Tuple", "Field", "Record"], "answer": 1},
                    {"question": "What does the term 'cascade' refer to in foreign key constraints?", "options": ["Automatically delete related rows", "Automatically update related rows", "Both 1 and 2", "None of the above"], "answer": 3},
                    {"question": "Which of the following is used to manage concurrency in DBMS?", "options": ["Locks", "Transactions", "Buffer management", "All of the above"], "answer": 4}
                ],
                "Hard": [
                    {"question": "What is the purpose of an ORM in DBMS?", "options": ["Object Relation Mapping", "Object Retrieval Mechanism", "Optimized Record Manager", "None of the above"], "answer": 1},
                    {"question": "What is a trigger in a database?", "options": ["A mechanism that automatically activates actions", "A mechanism to load data", "A data validation tool", "None of the above"], "answer": 1},
                    {"question": "Which of the following is an advantage of NoSQL over relational databases?", "options": ["Better support for complex queries", "Faster for large data", "Better for structured data", "All of the above"], "answer": 2},
                    {"question": "What is a stored procedure in DBMS?", "options": ["A set of SQL statements that can be stored and executed", "A backup utility", "A tool for data retrieval", "None of the above"], "answer": 1},
                    {"question": "Which is the correct order of steps in query optimization?", "options": ["Parse, Plan, Execute", "Parse, Execute, Plan", "Execute, Plan, Parse", "None of the above"], "answer": 1},
                    {"question": "Which of the following isolation levels can cause non-repeatable reads?", "options": ["Read Uncommitted", "Repeatable Read", "Serializable", "Read Committed"], "answer": 4},
                    {"question": "What is the advantage of using sharding in a distributed database?", "options": ["Improves query speed", "Provides backup of data", "Splits data for better management", "Reduces number of tables"], "answer": 3},
                    {"question": "What does SQL injection refer to?", "options": ["Injecting a new SQL command to manipulate data", "A method of data encryption", "Injecting a stored procedure", "None of the above"], "answer": 1},
                    {"question": "What is the advantage of using multi-version concurrency control?", "options": ["Faster data retrieval", "More accurate results during transactions", "No deadlocks", "Improved query performance"], "answer": 2},
                    {"question": "Which of the following is the main disadvantage of the ACID properties in DBMS?", "options": ["Requires more resources", "Slows down the system", "Difficult to implement", "None of the above"], "answer": 2}
                ]
            },
            "Computer Networks": {
                "Easy": [
                    {"question": "What does the acronym HTTP stand for?", "options": ["HyperText Transfer Protocol", "Hyper Tool Transfer Protocol", "Hyper Transaction Transfer Protocol", "Hyper Tool Transmission Protocol"], "answer": 1},
                    {"question": "Which device connects multiple networks together?", "options": ["Router", "Switch", "Hub", "Repeater"], "answer": 1},
                    {"question": "Which layer of the OSI model is responsible for routing?", "options": ["Network Layer", "Data Link Layer", "Application Layer", "Physical Layer"], "answer": 1},
                    {"question": "Which of the following is an example of a physical layer device?", "options": ["Router", "Hub", "Switch", "Bridge"], "answer": 2},
                    {"question": "Which protocol is used for sending email?", "options": ["SMTP", "HTTP", "FTP", "IP"], "answer": 1},
                    {"question": "In TCP/IP, which layer corresponds to the transport layer?", "options": ["TCP", "IP", "HTTP", "ARP"], "answer": 1},
                    {"question": "Which type of IP address is used for private networks?", "options": ["Public IP", "Private IP", "Loopback IP", "Multicast IP"], "answer": 2},
                    {"question": "What is the purpose of DNS?", "options": ["Translate domain names to IP addresses", "Manage email", "Transmit data over the internet", "Establish connections between devices"], "answer": 1},
                    {"question": "What is the maximum length of an Ethernet cable?", "options": ["100 meters", "50 meters", "200 meters", "150 meters"], "answer": 1},
                    {"question": "What type of protocol is FTP?", "options": ["Application Layer", "Transport Layer", "Network Layer", "Data Link Layer"], "answer": 1}
                ],
                "Medium": [
                    {"question": "Which of the following protocols is connection-oriented?", "options": ["TCP", "UDP", "ICMP", "IP"], "answer": 1},
                    {"question": "Which protocol is used to obtain an IP address from a DHCP server?", "options": ["DHCP", "TCP", "UDP", "HTTP"], "answer": 1},
                    {"question": "In IP addressing, how many bits are used for an IPv6 address?", "options": ["32", "64", "128", "256"], "answer": 3},
                    {"question": "Which of the following is used for error detection in data transmission?", "options": ["Checksum", "Data Link Layer", "Routing", "ARP"], "answer": 1},
                    {"question": "What is the purpose of the ARP protocol?", "options": ["Resolve IP addresses to MAC addresses", "Maintain IP addresses", "Route packets between networks", "Encrypt data"], "answer": 1},
                    {"question": "What does a subnet mask do in a network?", "options": ["Defines the network and host portions of an IP address", "Encrypts data", "Allocates IP addresses", "None of the above"], "answer": 1},
                    {"question": "Which type of switch supports VLANs?", "options": ["Managed switch", "Unmanaged switch", "Hub", "Router"], "answer": 1},
                    {"question": "Which of the following is an example of a link-state routing protocol?", "options": ["OSPF", "RIP", "BGP", "EIGRP"], "answer": 1},
                    {"question": "What is the purpose of the ICMP protocol?", "options": ["Error reporting", "Data transmission", "Routing", "Address allocation"], "answer": 1},
                    {"question": "Which of the following is used for NAT?", "options": ["Router", "Switch", "Hub", "Bridge"], "answer": 1}
                ],
                "Hard": [
                    {"question": "Which type of error does a cyclic redundancy check (CRC) detect?", "options": ["Bit errors", "Parity errors", "Routing errors", "Connection errors"], "answer": 1},
                    {"question": "Which protocol ensures secure communication over a network?", "options": ["SSL/TLS", "TCP", "UDP", "ARP"], "answer": 1},
                    {"question": "In IPv6, how many bytes does the address consist of?", "options": ["16 bytes", "32 bytes", "64 bytes", "128 bytes"], "answer": 1},
                    {"question": "What is the purpose of the BGP protocol?", "options": ["Inter-domain routing", "Intra-domain routing", "IP address allocation", "Error correction"], "answer": 1},
                    {"question": "What is the difference between a hub and a switch?", "options": ["Hub broadcasts data; switch routes data", "Hub routes data; switch broadcasts data", "Hub uses IP; switch uses MAC", "None of the above"], "answer": 1},
                    {"question": "Which of the following protocols uses port 443?", "options": ["HTTPS", "HTTP", "FTP", "SMTP"], "answer": 1},
                    {"question": "Which layer in the OSI model is responsible for flow control?", "options": ["Transport Layer", "Network Layer", "Data Link Layer", "Physical Layer"], "answer": 1},
                    {"question": "Which of the following techniques is used in congestion control?", "options": ["TCP slow start", "ICMP error messages", "IP fragmentation", "ARP"], "answer": 1},
                    {"question": "Which routing algorithm is used in the Internet's backbone?", "options": ["BGP", "RIP", "OSPF", "ICMP"], "answer": 1},
                    {"question": "What is the maximum size of a segment in TCP before it is fragmented?", "options": ["1460 bytes", "1500 bytes", "1024 bytes", "2048 bytes"], "answer": 1}
                ]
            },
            "Operating System": {
                "Easy": [
                    {"question": "What does the OSI model stand for?", "options": ["Open Systems Interconnection", "Operating System Integration", "Open System Interlink", "Operational System Infrastructure"], "answer": 1},
                    {"question": "Which of the following is an example of an operating system?", "options": ["Linux", "Python", "Chrome", "Java"], "answer": 1},
                    {"question": "Which component of an operating system manages memory?", "options": ["Memory Manager", "File Manager", "Processor Manager", "Device Manager"], "answer": 1},
                    {"question": "What does the kernel of an operating system do?", "options": ["Manages hardware resources", "Manages user interfaces", "Handles files", "Manages network protocols"], "answer": 1},
                    {"question": "Which type of operating system allows multiple users to work simultaneously?", "options": ["Multitasking", "Multiprocessing", "Multiuser", "Real-time"], "answer": 3},
                    {"question": "What is the purpose of a process scheduler?", "options": ["Allocate CPU time", "Manage system memory", "Manage file storage", "Track running processes"], "answer": 1},
                    {"question": "Which of the following is a popular open-source operating system?", "options": ["Linux", "Windows", "macOS", "Android"], "answer": 1},
                    {"question": "Which layer of the operating system interacts with hardware?", "options": ["Kernel", "Shell", "User interface", "File System"], "answer": 1},
                    {"question": "Which of the following is not an operating system?", "options": ["Windows", "Linux", "Android", "Python"], "answer": 4},
                    {"question": "What is the primary function of an operating system?", "options": ["Provide an interface for hardware", "Manage files and processes", "Provide networking capabilities", "All of the above"], "answer": 4}
                ],
                "Medium": [
                    {"question": "What is a system call in an operating system?", "options": ["A function for file operations", "A request from user-space to kernel-space", "A function for memory allocation", "A function for process management"], "answer": 2},
                    {"question": "Which of the following is the first part of the OS that loads when a computer starts?", "options": ["Bootloader", "Kernel", "Shell", "Process manager"], "answer": 1},
                    {"question": "Which process management concept refers to preventing one process from taking over the CPU indefinitely?", "options": ["Fair scheduling", "Multitasking", "Preemption", "Threading"], "answer": 3},
                    {"question": "Which of the following is a form of inter-process communication?", "options": ["Message passing", "Shared memory", "Pipes", "All of the above"], "answer": 4},
                    {"question": "What is a deadlock in an operating system?", "options": ["A state where no process can continue because it is waiting on another", "A situation where a process uses all CPU resources", "A form of memory leak", "An error in system calls"], "answer": 1},
                    {"question": "Which of the following is a key feature of a real-time operating system?", "options": ["Predictable behavior", "File system support", "Multitasking", "Graphical interface"], "answer": 1},
                    {"question": "What is a file descriptor in an operating system?", "options": ["A number that uniquely identifies a file in memory", "A pointer to a file in the operating system", "A command to open files", "None of the above"], "answer": 1},
                    {"question": "Which of the following is an example of a time-sharing system?", "options": ["Windows", "Linux", "macOS", "All of the above"], "answer": 4},
                    {"question": "Which technique does an operating system use to manage multiple processes in memory?", "options": ["Paging", "Segmentation", "Swapping", "All of the above"], "answer": 4},
                    {"question": "What is virtual memory?", "options": ["A system that uses hardware to extend available memory", "A part of the disk used as RAM", "A memory management technique", "All of the above"], "answer": 4}
                ],
                "Hard": [
                {"question": "Which algorithm is used for process scheduling in operating systems?", "options": ["Round-robin", "Shortest Job First", "Priority Scheduling", "All of the above"], "answer": 4},
                {"question": "What is the purpose of a semaphore in an operating system?", "options": ["To prevent race conditions", "To manage memory allocation", "To schedule processes", "To allocate file resources"], "answer": 1},
                {"question": "Which is the primary difference between a process and a thread?", "options": ["Threads share memory; processes do not", "Threads are independent; processes are not", "Processes can be suspended; threads cannot", "None of the above"], "answer": 1},
                {"question": "What is a page fault?", "options": ["When the requested page is not found in memory", "When a process exceeds its memory limit", "When a process accesses invalid memory", "None of the above"], "answer": 1},
                {"question": "Which of the following is not a form of memory allocation?", "options": ["Contiguous allocation", "Paged allocation", "Linked allocation", "Circular allocation"], "answer": 4},
                {"question": "What is a critical section problem?", "options": ["The inability to access a file system", "The inability to allocate memory", "The problem of ensuring mutual exclusion in shared resources", "The problem of process starvation"], "answer": 3},
                {"question": "What is the difference between user mode and kernel mode in operating systems?", "options": ["User mode is where user applications run; kernel mode handles system operations", "Kernel mode is restricted to memory management", "User mode executes hardware instructions", "None of the above"], "answer": 1},
                {"question": "Which technique is used to prevent deadlock in an operating system?", "options": ["Banker's algorithm", "Preemptive scheduling", "Deadlock avoidance", "All of the above"], "answer": 4},
                {"question": "What is the role of the file system in an operating system?", "options": ["Manages data storage and retrieval", "Allocates system resources", "Coordinates process scheduling", "Provides networking capabilities"], "answer": 1},
                {"question": "Which of the following is a key aspect of multi-core operating systems?", "options": ["Concurrent execution of multiple processes", "Better power management", "Improved performance", "All of the above"], "answer": 4}
            ]
            },
            "Data Structures": {
                "Easy": [
                    {"question": "What is an array?", "options": ["A collection of elements of the same type", "A collection of different types of elements", "A dynamic data structure", "None of the above"], "answer": 1},
                    {"question": "Which of the following is a linear data structure?", "options": ["Array", "Tree", "Graph", "None of the above"], "answer": 1},
                    {"question": "What is the time complexity of accessing an element in an array?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "answer": 1},
                    {"question": "What is a linked list?", "options": ["A collection of nodes where each node points to the next node", "A dynamic array", "A binary tree structure", "None of the above"], "answer": 1},
                    {"question": "Which data structure is used to implement a queue?", "options": ["Linked list", "Array", "Stack", "All of the above"], "answer": 2},
                    {"question": "What does the term 'push' mean in the context of a stack?", "options": ["Insert an element at the end", "Remove an element from the end", "Insert an element at the top", "Remove an element from the top"], "answer": 3},
                    {"question": "Which of the following is an example of a non-linear data structure?", "options": ["Array", "Stack", "Queue", "Tree"], "answer": 4},
                    {"question": "What is the time complexity of inserting an element at the beginning of a linked list?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "answer": 1},
                    {"question": "Which of the following data structures can be used to implement recursion?", "options": ["Stack", "Queue", "Array", "Linked list"], "answer": 1},
                    {"question": "Which of the following operations is not possible with a stack?", "options": ["Push", "Pop", "Peek", "Insert at any position"], "answer": 4}
                ],
                "Medium": [
                    {"question": "What is a hash table?", "options": ["A data structure that stores data in key-value pairs", "A type of array", "A tree structure", "A list of nodes"], "answer": 1},
                    {"question": "Which of the following is true about a binary search tree?", "options": ["Left child is less than parent", "Right child is less than parent", "Both left and right children are greater than parent", "None of the above"], "answer": 1},
                    {"question": "What is the worst-case time complexity of a quicksort algorithm?", "options": ["O(n^2)", "O(n log n)", "O(log n)", "O(n)"], "answer": 1},
                    {"question": "What is the space complexity of a recursive function using a stack?", "options": ["O(n)", "O(1)", "O(log n)", "O(n^2)"], "answer": 1},
                    {"question": "In a binary tree, what is the minimum number of nodes required to have a height of 3?", "options": ["7", "3", "5", "9"], "answer": 1},
                    {"question": "What is the primary advantage of a doubly linked list over a singly linked list?", "options": ["Can be traversed in both directions", "Requires less memory", "Supports faster deletion", "None of the above"], "answer": 1},
                    {"question": "Which of the following sorting algorithms has a best case time complexity of O(n)?", "options": ["Insertion sort", "Merge sort", "Quick sort", "Heap sort"], "answer": 1},
                    {"question": "Which of the following is the correct implementation of a breadth-first search (BFS)?", "options": ["Using a queue", "Using a stack", "Using recursion", "Using an array"], "answer": 1},
                    {"question": "What does the term 'collision' mean in a hash table?", "options": ["Two keys mapping to the same index", "A node having more than one child", "A node having no children", "None of the above"], "answer": 1},
                    {"question": "What is the worst-case time complexity of searching in a balanced binary search tree?", "options": ["O(log n)", "O(n)", "O(1)", "O(n^2)"], "answer": 1}
                ],
                "Hard": [
                    {"question": "What is the time complexity of the Floyd-Warshall algorithm?", "options": ["O(n^3)", "O(n^2)", "O(n log n)", "O(n)"], "answer": 1},
                    {"question": "Which of the following is the correct way to implement a priority queue?", "options": ["Using a heap", "Using an array", "Using a linked list", "Using a stack"], "answer": 1},
                    {"question": "What is the difference between a min-heap and a max-heap?", "options": ["Min-heap: Root is the smallest element; Max-heap: Root is the largest element", "Min-heap: Root is the largest element; Max-heap: Root is the smallest element", "Both heaps are identical", "None of the above"], "answer": 1},
                    {"question": "What is the time complexity of finding the shortest path using Dijkstra’s algorithm with a priority queue?", "options": ["O(E log V)", "O(V log E)", "O(V^2)", "O(E + V)"], "answer": 1},
                    {"question": "What is the main disadvantage of the quicksort algorithm?", "options": ["Worst-case time complexity of O(n^2)", "Not stable", "Needs additional memory", "None of the above"], "answer": 1},
                    {"question": "Which of the following data structures is most appropriate for implementing an LRU cache?", "options": ["Hash map and doubly linked list", "Stack", "Queue", "Array"], "answer": 1},
                    {"question": "What is the time complexity of performing a binary search on a sorted array?", "options": ["O(log n)", "O(n)", "O(n log n)", "O(1)"], "answer": 1},
                    {"question": "Which of the following graph traversal algorithms can be implemented recursively?", "options": ["DFS", "BFS", "Dijkstra", "Prim's"], "answer": 1},
                    {"question": "What is the space complexity of the merge sort algorithm?", "options": ["O(n)", "O(1)", "O(log n)", "O(n^2)"], "answer": 1},
                    {"question": "Which of the following sorting algorithms has the worst-case time complexity of O(n^2)?", "options": ["Bubble sort", "Quick sort", "Merge sort", "Heap sort"], "answer": 1}
                ]
            }
    }

    for category, difficulties in sample_questions.items():
        for difficulty, questions in difficulties.items():
            for question_data in questions:
                cursor.execute("""
                INSERT INTO questions (category, difficulty, question, options, answer) 
                VALUES (%s, %s, %s, %s, %s)""", 
                (category, difficulty, question_data["question"], json.dumps(question_data["options"]), question_data["answer"]))

    conn.commit()
    cursor.close()
    conn.close()


# User management functions
def register_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    username = input("Enter a new username: ").strip()
    password = input("Enter a password: ").strip()
    college = input("Enter your college name: ").strip()
    course = input("Enter your course name: ").strip()
    contact_number = input("Enter your contact number: ").strip()

    try:
        cursor.execute(
            "INSERT INTO users (username, password, college, course, contact_number) "
            "VALUES (%s, %s, %s, %s, %s)",
            (username, password, college, course, contact_number)
        )
        conn.commit()
        print("Registration successful! You can now log in.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def login_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome back, {username}!")
        return username
    else:
        print("Incorrect username or password.")
        return None

# fetch
def fetch_questions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    cursor.close()
    conn.close()
    return questions


# Hint system
def use_hint(question):
    options = json.loads(question["options"])  # Parse the options from JSON
    correct_answer = question["answer"]  

    incorrect_options = [opt for idx, opt in enumerate(options) if idx != correct_answer - 1]

    options_to_remove = random.sample(incorrect_options, 2)
    for opt in options_to_remove:
        options.remove(opt)

    print("\n50/50 Hint Used!")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

# Review incorrect answers
def review_incorrect_answers(incorrect_answers):
    print("\nReview Incorrect Answers:")
    for q in incorrect_answers:
        print(f"Question: {q['question']}")
        print(f"Your answer: {q['your_answer']} - Correct answer: {q['correct_answer']}")

# Daily Challenge
def generate_daily_challenge():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().date()
    cursor.execute("SELECT * FROM daily_challenge WHERE challenge_date = %s", (today,))
    daily_data = cursor.fetchone()

    if daily_data:
        return json.loads(daily_data['questions'])

    cursor.execute("SELECT * FROM questions")
    all_questions = cursor.fetchall()

    daily_questions = random.sample(all_questions, min(10, len(all_questions)))
    daily_questions_json = json.dumps(daily_questions)

    cursor.execute(
        "INSERT INTO daily_challenge (challenge_date, questions) VALUES (%s, %s)",
        (today, daily_questions_json)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return daily_questions

# Save achievements
def save_achievement(username, achievements):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        current_achievements = json.loads(user_data['achievements']) if user_data['achievements'] else []

        if achievements and achievements not in current_achievements:
            current_achievements.append(achievements)
            cursor.execute("UPDATE users SET achievements = %s WHERE username = %s", (json.dumps(current_achievements), username))
            print("Achievement added!")
    else:
        print("User not found. Please check the system.")
    
    conn.commit()
    cursor.close()
    conn.close()

# Main quiz function
def play_quiz(username, questions, timed=False):
    score = 0
    incorrect_answers = []
    hints_used = 0
    total_questions = len(questions)
    achievements = []  

    if total_questions < 10:
        print(f"\nOnly {total_questions} questions available for this category and difficulty. Proceeding with all available questions.")
        num_questions = total_questions  
    else:
        num_questions = 10  

    selected_questions = random.sample(questions, num_questions)

    for idx, q in enumerate(selected_questions, start=1):
        print(f"\nQuestion {idx}: {q['question']}")
        options = json.loads(q["options"])  
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        if timed:
            print("\nYou have 10 seconds to answer this question.")
            start_time = time.time()

        while True:
            try:
                user_choice = input("Enter your choice (or 'h' for hint): ").strip()

                if user_choice.lower() == 'h':
                    if hints_used < 2:
                        use_hint(q)
                        hints_used += 1
                    else:
                        print("You have used all your hints.")
                    continue

                user_choice = int(user_choice)
                if user_choice < 1 or user_choice > 4:
                    print("Invalid choice. Please select a number between 1 and 4.")
                    continue

                if user_choice == q["answer"]:
                    print("Correct!")
                    score += 1
                else:
                    print("Wrong!")
                    incorrect_answers.append({
                        "question": q["question"],
                        "your_answer": user_choice,
                        "correct_answer": q["answer"]
                    })
                break 

            except ValueError:
                print("Invalid input. Please enter a valid number between 1 and 4.")
                
            if timed and time.time() - start_time > 10:
                print("Time's up! Moving to the next question.")
                break

    print(f"\nQuiz finished! Your score: {score}/{num_questions}")

    if score == num_questions:
        achievements.append("Perfect Score")
    if hints_used == 0:
        achievements.append("Hint Master")

    save_to_leaderboard(username, score)

    if incorrect_answers:
        review_incorrect_answers(incorrect_answers)

    if achievements:
        save_achievement(username, achievements)
        print("\nAchievements unlocked:")
        for achievement in achievements:
            print(f"🏆 {achievement}")

# Save score to leaderboard
def save_to_leaderboard(username, score):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  

    cursor.execute("SELECT * FROM leaderboard WHERE username = %s", (username,))
    existing_entry = cursor.fetchone()

    if existing_entry:
        if existing_entry['score'] < score:
            cursor.execute("UPDATE leaderboard SET score = %s WHERE username = %s", (score, username))
            print("New high score!")
    else:
        cursor.execute("INSERT INTO leaderboard (username, score) VALUES (%s, %s)", (username, score))
        print("Score added to leaderboard!")

    conn.commit()
    cursor.close()
    conn.close()

# Show leaderboard
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10")
        leaderboard = cursor.fetchall()
        return leaderboard if leaderboard else []
    except mysql.connector.Error as err:
        print(f"Error fetching leaderboard: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

# Introduction
def intro():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 1")
    leaderboard = cursor.fetchall()

    print("\n🎉 Welcome to QuizQuest! 🧠✨")
    print("Where questions are tough, but you're tougher! 💪\n")
    print("Think you've got what it takes to outsmart the quiz and claim the crown? 👑")
    print("We’ve got:")
    print("🔥 Brain-tickling questions across Easy, Medium, and Hard levels.")
    print("🤔 Trivia that'll make you say, \"Oh, I *should've* known that!\"")
    print("🏆 A leaderboard that showcases the sharpest minds around.\n")

    if leaderboard:
        top_player = leaderboard[0]['username']
        top_score = leaderboard[0]['score']
        print(f"📜 **Leaderboard Update:**")
        print(f"🥇 **Top Spot:** {top_player} is ruling the roost with a score of {top_score}! Think you can dethrone them? 😏")
    else:
        print("📜 **Leaderboard Update:**")
        print("🤷‍♂️ **No one at the top?** That’s your cue! Jump in and take the lead—be the first name in lights!\n")

    print("So buckle up, brainiac—it’s time to quiz and conquer! 🚀")
    print("Let the games begin!\n")

    cursor.close()
    conn.close()


def display_achievements(username):

    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database. Please try again later.")
        return

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT achievements FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data:
            achievements_data = user_data.get('achievements')
            if achievements_data:
                try:
                    achievements = json.loads(achievements_data)
                    if achievements:
                        print("\n🏆 Your Achievements:")
                        for idx, achievement in enumerate(achievements, start=1):
                            print(f"{idx}. {achievement}")
                    else:
                        print("\nYou haven't unlocked any achievements yet. Keep playing to earn some!")
                except json.JSONDecodeError:
                    print("Error decoding achievements data. Please contact support.")
            else:
                print("\nNo achievements recorded for this user.")
        else:
            print("User data not found. Please check the system.")
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    
    finally:
        cursor.close()
        conn.close()


# Main menu function
def main_menu():
    initialize_database()
    intro()
    username = None

    while True:
        print("""
        Main Menu:
        1. Register
        2. Login
        3. Play Quiz
        4. Daily Challenge
        5. Leaderboard
        6. Achievements
        7. Exit
        """)
        
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Invalid choice. Please enter a number.")
            continue

        if choice == 1:
            register_user()
        elif choice == 2:
            username = login_user()
        elif choice == 3:
            if not username:
                print("Please log in to play the quiz.")
                continue
            category_choice = input("\nChoose category (1. DBMS, 2. Computer Networks, 3. Operating System, 4. Data Structures): ").strip()
            categories = {1: 'DBMS', 2: 'Computer Networks', 3: 'Operating System', 4: 'Data Structures'}
            category = categories.get(int(category_choice), None)

            if not category:
                print("Invalid category choice.")
                continue

            difficulty_choice = input("\nChoose difficulty (1. Easy, 2. Medium, 3. Hard): ").strip()
            difficulties = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
            difficulty = difficulties.get(int(difficulty_choice), None)

            if not difficulty:
                print("Invalid difficulty choice.")
                continue

            questions = fetch_questions()
            filtered_questions = [q for q in questions if q['category'] == category and q['difficulty'] == difficulty]

            if filtered_questions:
                play_quiz(username, filtered_questions)
            else:
                print(f"No questions available for the category {category} and difficulty {difficulty}. Please try again later.")
        elif choice == 4:
            if not username:
                print("Please log in to play the daily challenge.")
                continue
            daily_challenge = generate_daily_challenge()
            play_quiz(username, daily_challenge)
        elif choice == 5:
            print("\n🏆 Leaderboard 🏆")
            leaderboard = get_leaderboard()
            if leaderboard:
                for idx, entry in enumerate(leaderboard, start=1):
                    print(f"{idx}. {entry['username']} - {entry['score']} points")
            else:
                print("No leaderboard data available.")
        elif choice == 6:
            if not username:
                print("Please log in to view your achievements.")
                continue
            display_achievements(username)
        elif choice == 7:
            print("Thank you for playing! See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()