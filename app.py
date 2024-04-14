from IPython.display import display, HTML

# HTML and CSS code for the UI
html_code = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-image: url('football.jpg'); /* Replace 'football_background.jpg' with your image path */
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .input-field {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
            color: #333;
            outline: none;
        }
        .btn {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: #007bff; /* Blue color */
            color: white;
            cursor: pointer;
            outline: none;
        }
        .btn:hover {
            background: #0056b3; /* Darker blue color on hover */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Football Match Prediction</h1>
        <form>
            <input type="text" class="input-field" placeholder="Enter Team A">
            <input type="text" class="input-field" placeholder="Enter Team B">
            <button type="submit" class="btn">Predict</button>
        </form>
    </div>
</body>
</html>
'''

# Display the HTML code
display(HTML(html_code))
