# COMF

COMF is a Python-based open-source thermal analysis software. It is essentially a tool to obtain kinetic information from thermogravimetric analysis (TGA) data to characterise solid materials, particularly of pharmaceutical, petrochemical, food and environmental interest. It basically provides a full kinetic analysis of these data, including the determination of the **reaction model** and calculation of the **activation energy**, i.e. generally the kinetic triplet, for isothermal solid-state reactions. It can be used to investigate physicochemical phenomena, such as phase transitions, desolvation/dehydration of pharmaceutical solvates/hydrates, absorption, adsorption and desorption, thermal decomposition, and solid-gas reactions, e.g. oxidation or reduction. This software is based on two methods:

1. the **Co**mprehensive **M**odel-**F**itting **M**ethod developed by [Y. Vasilopoulos et al](https://www.mdpi.com/2073-4352/10/2/139/htm) (here you can find also what models are supported by this software)
2. and the integral isoconversional method

## Installation

Clone this repository using [GitHub](https://help.github.com/en/enterprise/2.13/user/articles/cloning-a-repository)

```bash
git clone https://github.com/vasilogi/COMF.git
```

or simply download it!

## Usage

To use the software, you need to apply the following steps:

1. Create CSV files for your TGA data
2. Implement the isoconversional method
3. Implement COMF
4. Determine the kinetic triplet

### CSV data format

Add your data to the [data](./data) directory in a CSV format. The CSV file must include at least 3 columns, namely **Time (min)**, **Temperature (C)**, and **Conversion**. Filenames do not matter but headers do. To properaly prepare your csv data file check out the existing [example](./data/80_0_Celcius.csv).

### Implement the isoconversional method

Open the [isoconversional analysis Jupyter notebook](./iso-analysis.ipynb).



```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
