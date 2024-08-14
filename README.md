## Machine Vision Project
### Objective
-  Establish a grounding in the requisite areas of Linear Algebra and the NumPy library to distinguish hand-written digits in the MNIST dataset.
- Apply those techniques to a Machine Vision problem to differentiate real-world objects, such as dogs and cats.

### Tech Stack
- Python
- NumPy, PIL library
- html, css

### Test instructions
Method 1
```
python main.py
Enter value for dataSet: mnist
Enter value for classes: 0,1
Enter value for imgSize: 28,28
Enter value for threshold_ratio: 0.01

python main.py
Enter value for dataSet: imagenet
Enter value for classes: 00153,00283
Enter value for imgSize: 100,100
Enter value for threshold_ratio: 0.01

```
Method 2
```
python main.py dataSet=mnist classes=0,1 imgSize="28,28" threshold_ratio=0.01

python main.py dataSet=ImageNet classes="00153,00283" imgSize="100,100" threshold_ratio=0.01
```

#### Run the unit tests
```
python test.py
```