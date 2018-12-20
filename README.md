Dataset on Globus:
https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&origin_path=%2Fschwarting%2F

Original Dataset:
https://data.caltech.edu/records/1103


Goals for the MatAutoEncode Repo:

- Get dataset into MDF, make sure that any user can pull it down and easily access both spectra and image

- Implement MARS to compute this dataset, possibly build in a Bayesian component as a probability density function for the distribution of the band gap across the spectrum (?).

- Run MARS on the entire set, output to a csv for easy access.

- Build an autoencoder just like Stein's, then build a different autoencoder that also incorporates composition and band gap information (depending on the direction). See if we can get an improved performance.

- Construct binaries/ternaries/quaternaries colored by band gap as well as average color of the sample. Compare these with experimental phase diagrams in ICSD and computational phase diagrams in Materials Project.

- Modify MARS methodologies to detect multiple band gaps.

- Color analysis on samples to determine possible oxidation states or annealing conditions (stretch?).

- Other? (Ben please add here)
