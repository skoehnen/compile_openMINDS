import openminds
import generator

om = openminds.OpenMINDS()
copyright_class = generator.generate(om.COPYRIGHT)

print(vars(copyright_class))
copyright_obj = copyright_class(1,2,3,4)

print(copyright_obj.year)
