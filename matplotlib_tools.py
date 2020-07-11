from matplotlib import pyplot as plt


def scroll():
    fig = plt.figure()

    def scrollEvent(event):
        # axtemp -> class 'matplotlib.axes._axes.Axes'
        axtemp = event.inaxes

        try:
            x_min, x_max = axtemp.get_xlim()
            fanwei = (x_max - x_min) / 10

            if event.button == 'up':
                axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
                # print('up')
            elif event.button == 'down':
                axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
                # print('down')

            # 重新根據 xlim 繪製圖片
            fig.canvas.draw_idle()
        except AttributeError:
            # 若在
            # AttributeError: 'NoneType' object has no attribute 'get_xlim'
            pass

    fig.canvas.mpl_connect('scroll_event', scrollEvent)


if __name__ == "__main__":
    import numpy as np

    scroll()
    x = list(range(50))
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()
