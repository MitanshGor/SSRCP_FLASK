# SSRCP_FLASK
Flask API's for carla simulation API

# CARLA Simulator Setup Instructions  

This guide will walk you through setting up the CARLA Simulator and integrating it with the SSRCP_FLASK application.  

## Prerequisites  

- Ensure you have Python 3.7+ installed.  
- Install necessary dependencies for CARLA and Flask.  
- Check your system meets CARLA's requirements (refer to the CARLA documentation).  
- If using a VM or remote server, configure SSH tunneling as needed.  


# MongoDB Setup for SSRCP  

1. Ensure MongoDB is installed and running on `localhost:27017`.  
2. Create a database named `SSRCP`.  
3. Inside the `SSRCP` database, create a collection named `robot`.  
4. Use the provided Python script to interact with the database and collection.  


---

## Step 1: Setup CARLA Simulator  

1. Navigate to the root directory of this repository.  
2. Locate the **`CARLA_SETUP.pdf`** file in the repository's root directory.  
3. Follow the instructions in **`CARLA_SETUP.pdf`** to download and set up the CARLA simulator on your system.  

---

## Step 2: Clone the SSRCP_FLASK Application  

1. Once CARLA is set up, clone the **SSRCP_FLASK** application into the root folder of the CARLA project directory.  
   ```bash  
   git clone <SSRCP_FLASK_REPO_URL>

Replace <SSRCP_FLASK_REPO_URL> with the actual repository URL for SSRCP_FLASK.

Ensure the SSRCP_FLASK application is located inside the CARLA simulator's root folder


## Step 3: Configure SSH Tunneling (if applicable)

If you are using a Virtual Machine (VM) or a remote server instead of your local machine, you will need to set up SSH tunneling.
SSH Tunneling Steps:
On your local machine, execute the following command to create an SSH tunnel:

```bash
  ssh -f -N -R  27017:localhost:27017 VM_USER@VM_IP_ADDRESS
  ssh -f -N -R  5000:localhost:5000 VM_USER@VM_IP_ADDRESS

```

Verify the tunnel is established and accessible on your local system.

   
## Running the Flask Application  

This guide provides the steps to set up and run the Flask application.  

---

### Prerequisites  

- Python 3.7+ installed on your system.  
- Virtual environment (venv) module installed.  

---

### Steps to Run the Flask Application  

#### Step 1: Create and Activate the Virtual Environment  

1. Navigate to the root directory of the Flask application:  
   ```bash  
   cd SSRCP_FLASK  

Create a virtual environment:

bash
Copy code
```bash
  python -m venv venv
```
Activate the virtual environment:
```bash
  source venv/bin/activate  
```

Run Flask
```bash
python run.py  
```

The application should now be running locally. You can access it by navigating to: `http://127.0.0.1:5000`






