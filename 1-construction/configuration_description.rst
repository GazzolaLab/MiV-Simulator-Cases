******************
YAML Configuration 
******************

The MiV-Simulator leverages a YAML-based configuration format to declaratively describe complex neural systems. The user-specified configuration files are used to generate concrete instantiations of the system used in the simulation. 
For example, a YAML user configuration may describe the number and distribution of neurons which is used during network construction to determine the exact sampled soma positions.

The different configuration templates that are used for simulation construction are described below.


Simulation Configuration
========================

.. literalinclude:: config/Microcircuit_Small.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Connection_Velocity.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Definitions.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Geometry_Small.yaml
   :linenos:
   :language: yaml
   :caption:

Synapse / Dentrites Configuration
=================================

.. literalinclude:: config/Microcircuit_Connections.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Axon_Extent.yaml
   :linenos:
   :language: yaml
   :caption:


.. literalinclude:: config/OLM_synapse_density.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/PVBC_synapse_density.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/PYR_synapse_density.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/PYR_SoldadoMagraner.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Synapse_Parameter_Rules.yaml
   :linenos:
   :language: yaml
   :caption:

Input / Stimulation Configuration
=================================

.. literalinclude:: config/Input_Configuration.yaml
   :linenos:
   :language: yaml
   :caption:


Post-Process Configuration
==========================

.. literalinclude:: config/Recording.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Analysis_Configuration.yaml
   :linenos:
   :language: yaml
   :caption:

Miscellaneous Configuration
===========================

.. literalinclude:: config/Random.yaml
   :linenos:
   :language: yaml
   :caption:

.. literalinclude:: config/Global.yaml
   :linenos:
   :language: yaml
   :caption:
