```{=latex}
\clearpage
\appendix
\part*{Appendices}
\addcontentsline{toc}{part}{Appendices}
```

# List of symbols {#sec:symbols}

| Symbol | Meaning | Unit |
|--------|---------|------|
| $x, y, z$ | horizontal coordinates and elevation (positive up) | m |
| $t$, $\Delta t$ | time and time step | s |
| $\Delta x, \Delta y$ | grid spacings | m |
| $u, v$, $\mathbf u$ | velocity components and vector | m/s |
| $h$, $d$ | water depth | m |
| $\eta$ | free-surface elevation, setup | m |
| $g$ | gravitational acceleration, 9.81 | m/s$^2$ |
| $\rho$, $\rho_s$ | water and sediment (or rock) density | kg/m$^3$ |
| $\Delta$ | relative buoyant density $\rho_s/\rho - 1$ | - |
| $\nu$, $\nu_t$ | kinematic and eddy viscosity | m$^2$/s |
| $k$, $\varepsilon$, $\omega$ | turbulent kinetic energy, dissipation, specific dissipation | m$^2$/s$^2$, m$^2$/s$^3$, 1/s |
| $C_s$ | Smagorinsky constant | - |
| $\sigma(x)$, $L_\mathrm{sp}$ | sponge damping rate and thickness | 1/s, m |
| $H$, $H_s$, $H_{m0}$, $H_b$ | wave height, significant height, spectral height, breaking height | m |
| $T$, $T_p$, $T_{m-1,0}$ | period, peak period, spectral period | s |
| $L$, $L_0$, $k$, $\omega$ | wavelength, deep-water wavelength, wavenumber, angular frequency | m, m, 1/m, 1/s |
| $c$, $c_g$ | phase and group celerity | m/s |
| $\xi$ | surf similarity (Iribarren) number | - |
| $U$ | Ursell number | - |
| $S(f)$, $m_n$ | variance density spectrum, spectral moment | m$^2$/Hz |
| $\alpha$, $\beta$ | structure slope angle; wave obliquity or beach slope | rad or deg |
| $D_{n50}$, $M_{50}$ | nominal stone diameter and median mass | m, kg |
| $P$, $S$, $N$ | notional permeability, damage level, number of waves | - |
| $K_D$ | Hudson stability coefficient | - |
| $R_c$ | crest freeboard | m |
| $q$ | mean overtopping discharge | l/s/m |
| $\gamma_f, \gamma_\beta, \gamma_b, \gamma_v$ | EurOtop roughness, obliquity, berm, and wall factors | - |
| $p_1, p_3, p_4, p_u$ | Goda pressures and uplift | kPa |
| $K_r$, $K_d$ | reflection and disturbance coefficients | - |
| $C_d$, $C_m$ | Morison drag and inertia coefficients | - |
| $KC$ | Keulegan-Carpenter number | - |
| $U_c$, $U_m$, $U_{cw}$ | current, near-bed orbital velocity, current share | m/s, m/s, - |
| $S$, $S_\mathrm{eq}$ | scour depth, equilibrium scour depth | m |
| $D_e$ | effective pier diameter | m |
| $\theta$, $\theta_{cr}$ | Shields parameter and its critical value | - |
| $d_{50}$, $D_*$, $w_s$ | median grain size, dimensionless grain size, fall velocity | m, -, m/s |
| $\phi'$, $K_a$, $K_0$ | friction angle, active and at-rest pressure coefficients | deg, - |
| $n$, $K$, $S_f$ | Manning coefficient, conveyance, friction slope | s/m$^{1/3}$, m$^3$/s, - |
| $Fr$ | Froude number | - |
| $F_{nh}$ | depth Froude number of a ship | - |
| $C_b$, $L_{pp}$, $B$, $T$ | block coefficient, length between perpendiculars, beam, draught | -, m, m, m |
| $C_m, C_e, C_s, C_c$ | PIANC berthing factors | - |
| $A$ | Dean profile scale | m$^{1/3}$ |
| $\varepsilon$ | longshore diffusivity (one-line model) | m$^2$/s |
| $Q$, $K_\mathrm{cerc}$ | longshore transport and CERC coefficient | m$^3$/s |
| $u$, $\sigma$, $\xi$, $\lambda$ | threshold, scale, shape, and rate of an extreme value fit | - |

# Engineering references {#sec:refs}

The design relations implemented in pyCoastal, as cited in the module
docstrings.

- Barrass, C. B. (1979). A unified approach to squat calculations for ships. *PIANC Bulletin*, 32.
- Breusers, H. N. C., Nicollet, G., and Shen, H. W. (1977). Local scour around cylindrical piers. *Journal of Hydraulic Research*, 15(3), 211-252.
- Brolsma, J. U., Hirs, J. A., and Langeveld, J. M. (1977). On fender design and berthing velocities. *PIANC 24th Congress*.
- BS 6349-4 (2014). *Maritime works. Code of practice for design of fendering and mooring systems*. British Standards Institution.
- Chorin, A. J. (1968). Numerical solution of the Navier-Stokes equations. *Mathematics of Computation*, 22(104), 745-762.
- Chow, V. T. (1959). *Open-Channel Hydraulics*. McGraw-Hill.
- CIRIA, CUR, and CETMEF (2007). *The Rock Manual: The Use of Rock in Hydraulic Engineering*, 2nd ed. CIRIA C683.
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*. Springer.
- Dean, R. G., and Dalrymple, R. A. (1991). *Water Wave Mechanics for Engineers and Scientists*. World Scientific.
- DNV (2010). *DNV-RP-C205: Environmental Conditions and Environmental Loads*. Det Norske Veritas.
- EurOtop (2018). *Manual on Wave Overtopping of Sea Defences and Related Structures*, 2nd ed. Van der Meer, J. W., Allsop, N. W. H., Bruce, T., De Rouck, J., Kortenhaus, A., Pullen, T., Schüttrumpf, H., Troch, P., and Zanuttigh, B.
- FEMA (2005). *Guidelines and Specifications for Flood Hazard Mapping Partners*. Federal Emergency Management Agency.
- Ferziger, J. H., and Perić, M. (2002). *Computational Methods for Fluid Dynamics*. Springer.
- Froehlich, D. C. (1989). Local scour at bridge abutments. *Proceedings, ASCE National Hydraulic Conference*, 13-18.
- Goda, Y. (1974). New wave pressure formulae for composite breakwaters. *Proceedings of the 14th International Conference on Coastal Engineering*, 1702-1720.
- Goda, Y. (2010). *Random Seas and Design of Maritime Structures*, 3rd ed. World Scientific.
- Gottlieb, S., Shu, C.-W., and Tadmor, E. (2001). Strong stability-preserving high-order time discretization methods. *SIAM Review*, 43(1), 89-112.
- Hasselmann, K., et al. (1973). Measurements of wind-wave growth and swell decay during the Joint North Sea Wave Project (JONSWAP). *Deutsche Hydrographische Zeitschrift*, A8(12).
- Henderson, F. M. (1966). *Open Channel Flow*. Macmillan.
- Hosking, J. R. M., and Wallis, J. R. (1997). *Regional Frequency Analysis: An Approach Based on L-Moments*. Cambridge University Press.
- Hudson, R. Y. (1959). Laboratory investigation of rubble-mound breakwaters. *Journal of the Waterways and Harbors Division*, 85(3), 93-121.
- Hydrologic Engineering Center (2016). *HEC-RAS River Analysis System, Hydraulic Reference Manual, Version 5.0*. US Army Corps of Engineers.
- James, W. R. (1975). *Techniques in evaluating suitability of borrow material for beach nourishment*. Technical Memorandum 60, US Army Coastal Engineering Research Center.
- Kriebel, D. L., Kraus, N. C., and Larson, M. (1991). Engineering methods for predicting beach profile response. *Proceedings of Coastal Sediments '91*, 557-571.
- Lagasse, P. F., et al. (2009). *Bridge Scour and Stream Instability Countermeasures*, HEC-23, 3rd ed. Federal Highway Administration.
- Laursen, E. M. (1960). Scour at bridge crossings. *Journal of the Hydraulics Division*, 86(2), 39-54.
- Launder, B. E., and Spalding, D. B. (1974). The numerical computation of turbulent flows. *Computer Methods in Applied Mechanics and Engineering*, 3(2), 269-289.
- LeVeque, R. J. (2002). *Finite Volume Methods for Hyperbolic Problems*. Cambridge University Press.
- Morison, J. R., O'Brien, M. P., Johnson, J. W., and Schaaf, S. A. (1950). The force exerted by surface waves on piles. *Petroleum Transactions, AIME*, 189, 149-154.
- Pelnard-Considère, R. (1956). Essai de théorie de l'évolution des formes de rivage en plages de sable et de galets. *4èmes Journées de l'Hydraulique*, Question III, 289-298.
- PIANC (2002). *Guidelines for the Design of Fender Systems*. Report of Working Group 33, Maritime Navigation Commission.
- PIANC (2014). *Harbour Approach Channels: Design Guidelines*. Report 121.
- Pierson, W. J., and Moskowitz, L. (1964). A proposed spectral form for fully developed wind seas. *Journal of Geophysical Research*, 69(24), 5181-5190.
- Pope, S. B. (2000). *Turbulent Flows*. Cambridge University Press.
- Richardson, E. V., and Davis, S. R. (2001). *Evaluating Scour at Bridges*, HEC-18, 4th ed. Federal Highway Administration.
- Seelig, W. N., and Ahrens, J. P. (1981). *Estimation of wave reflection and energy dissipation coefficients for beaches, revetments, and breakwaters*. Technical Paper 81-1, US Army Coastal Engineering Research Center.
- Smagorinsky, J. (1963). General circulation experiments with the primitive equations. *Monthly Weather Review*, 91, 99-164.
- Soulsby, R. L. (1997). *Dynamics of Marine Sands*. Thomas Telford.
- Soulsby, R. L., and Whitehouse, R. J. S. (1997). Threshold of sediment motion in coastal environments. *Proceedings of Pacific Coasts and Ports '97*, 149-154.
- Stockdon, H. F., Holman, R. A., Howd, P. A., and Sallenger, A. H. (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering*, 53(7), 573-588.
- Sumer, B. M., Christiansen, N., and Fredsøe, J. (1992). Time scale of scour around a vertical pile. *Proceedings of the 2nd International Offshore and Polar Engineering Conference*, 308-315.
- Sumer, B. M., and Fredsøe, J. (2001). Scour around pile in combined waves and current. *Journal of Hydraulic Engineering*, 127(5), 403-411.
- Sumer, B. M., and Fredsøe, J. (2002). *The Mechanics of Scour in the Marine Environment*. World Scientific.
- Sumer, B. M., Fredsøe, J., and Christiansen, N. (1992). Scour around vertical pile in waves. *Journal of Waterway, Port, Coastal, and Ocean Engineering*, 118(1), 15-31.
- Takahashi, S., Tanimoto, K., and Shimosako, K. (1994). A proposal of impulsive pressure coefficient for design of composite breakwaters. *Proceedings of the International Conference on Hydro-Technical Engineering for Port and Harbor Construction*, 489-504.
- US Army Corps of Engineers (1984). *Shore Protection Manual*. Coastal Engineering Research Center.
- US Army Corps of Engineers (2002). *Coastal Engineering Manual*, EM 1110-2-1100.
- Van der Meer, J. W. (1988). *Rock slopes and gravel beaches under wave attack*. PhD thesis, Delft University of Technology; Delft Hydraulics Publication 396.
- Van Rijn, L. C. (1984). Sediment transport, part I: bed load transport. *Journal of Hydraulic Engineering*, 110(10), 1431-1456.
- Vasco Costa, F. (1964). The berthing ship: the effect of impact on the design of fenders and other structures. *The Dock and Harbour Authority*, 45.
- Wheeler, J. D. (1970). Method for calculating forces produced by irregular waves. *Journal of Petroleum Technology*, 22(3), 359-367.
- Wilcox, D. C. (1998). *Turbulence Modeling for CFD*. DCW Industries.
- Xie, S. L. (1981). *Scouring patterns in front of vertical breakwaters and their influence on the stability of the foundations of the breakwaters*. Delft University of Technology.
- Yarnell, D. L. (1934). *Bridge piers as channel obstructions*. Technical Bulletin 442, US Department of Agriculture.
