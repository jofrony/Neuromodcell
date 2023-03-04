from neuromodcell.modulation_set import DefineModulation


def test_DefineModulation():
    _ = DefineModulation()

    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    _ = DefineModulation(parameterID=parameterID,cell_name=cell_name,cell_dir=cell_dir,
                         output_dir=output_dir,population=population,tstop=tstop,time_step=time_step)


if __name__ == "__main__":
    test_DefineModulation()
