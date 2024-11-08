import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import calendar
import numpy as np
import matplotlib as mpl

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
#df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')
df = pd.read_csv('fcc-forum-pageviews.csv')
df = df.astype({'date':'datetime64'})
df = df.set_index(['date'])

# Clean data
df = df[(df['value'] <= df['value'].quantile(0.975)) &
        (df['value'] >= df['value'].quantile(0.025))]
#print(df.index.min())
#print(df.index.max())

def draw_line_plot():
    # Draw line plot
    font = {'family' : 'sans',
            'weight' : 'bold',
            'size'   : 22}

    plt.rc('font', **font)

    fig, ax = plt.subplots(figsize=(30, 10))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    #plt.minorticks_off()
    sns.lineplot(df, legend=False, palette=['red'])


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    #df_bar['month'] = df_bar['month'].apply(lambda row: calendar.month_name[row] )
    #df_bar = df_bar.groupby(['year','month'], as_index=False).mean()
    df_bar = df_bar.groupby(['year','month']).mean()
    
    df_bar = df_bar.unstack(fill_value=0)
    
    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(50,25)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    month_name = [calendar.month_name[m] for m in np.arange(12)+1]
    plt.legend(month_name, title="Months")

    #sns.set_theme(font_scale=2)
    #sns.barplot(data=df_bar, x='year', y='value', hue='month', palette='Paired', hue_order=month_name)
        
    #handles = plt.legend().legend_handles
    #newHandles = []
    # for i, handle in enumerate(handles):
    #     color = handle.get_facecolor()
    #     label = handle.get_label()
    #     #print(color)
    #     #handle = Line2D([0], [0], marker='o')
    #     circle = Line2D([0], [0], marker='o', color=color, label = label)
    #     circle.set_linewidth(0)
    #     circle.set_markersize(20)
    #     newHandles.append(circle)
    #     #handle.set_facecolor(colors[i])
    #     #handle.set_hatch("o")
    #     #handle.set_alpha(0.7)


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box['month_num'] = [d.month for d in df_box.date]
    df_box.sort_values('month_num', inplace=True)

    #print(df_box)

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(50, 20))
    
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    sns.boxplot(ax=ax1, data=df_box, x='year', y='value', palette='Set1')
    
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    sns.boxplot(ax=ax2, data=df_box, x='month', y='value', palette='Set1')
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
