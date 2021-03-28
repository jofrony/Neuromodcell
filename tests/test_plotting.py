import neuromodulation.plotting as npl

def test_plot_comparison():

    npl.plot_comparison(control = { "mean" : 3.56, "std" : 0.88},\
                        control_sim = [[3]],\
                        modulated = { "mean" : 10.00, "std" : 4.73},\
                        modulated_sim = [[5]],\
                        x_ticks = ['Model 1'],\
                        ylabel = '',\
                        title = '',\
                        dir_path = '',\
                        num_models = 1,\
                        save=True,\
                        filename='t.pdf')
