import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python settemp.py <temperature>")
        sys.exit(1)

    try:
        new_temp = float(sys.argv[1])
    except ValueError:
        print("Invalid temperature value. Please provide a number.")
        sys.exit(1)

    temp_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_live.txt')

    with open(temp_file_path, 'w') as f:
        f.write(str(new_temp))

    print(f"Live temperature has been set to {new_temp}")
