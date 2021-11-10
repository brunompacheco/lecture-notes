import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('range_results.csv')
    df.plot(x='Qinj_max', y='OilProduction', legend=False, title='Oil Production')
    plt.show()
