import matplotlib.pyplot as plt
import csv

csv_file = "hash_table.csv"

data1 = []
data2 = []
data3 = []
data4 = []


with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        data1.append(float(row[1]))
        data2.append(float(row[2]))
        data3.append(float(row[3]))
        data4.append(float(row[4]))

plt.plot(data1, label="Brute-Force")
plt.plot(data2, label="Rehashing")
plt.plot(data3, label="hash function optimization")
plt.plot(data4, label="Rehashing + hash function optimization")


plt.title("time Comparison")
plt.legend(borderaxespad=1, fontsize=7)

plt.xlabel("data")
plt.ylabel("Time(sec)")

plt.savefig("hash_table.png")
plt.show()
