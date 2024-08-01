import numpy as np
import requests  # Example of another package

a = np.array([1, 2, 3])
print(a)



a = np.array([1, 2, 3])
response = requests.get('https://api.github.com')
print(a, response.status_code)
