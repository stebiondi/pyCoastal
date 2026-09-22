# Preface {.unnumbered}

pyCoastal started as the culmination of my academic journey in numerical
modeling, fluid dynamics, and hydraulics. Students often believe that
numerical models are overwhelmingly complex tools; however, their structure
follows recurrent patterns common to many modeling frameworks. When properly
configured and validated, these models can reproduce real-world phenomena,
provide insight, and let us explore scenarios beyond direct observation.
Some researchers prefer to work in the analytical domain, which has its own
advantages and limitations, and I admire those who can capture the
complexity of natural processes through concise formulations that, even if
simplified, reflect the essence of how the world operates.

Since the first edition of this manual the package has grown in a different
direction as well. Next to the numerical framework it now carries a complete
design chain: a wave record becomes a design condition, the design condition
sizes a structure, and the structure comes out as a dimensioned drawing with
its quantities and its specification notes. Every relation names its
source, states its range of validity, and says so when it is pushed outside
that range. A browser version of the design modules, the Coastal Design
Bench, puts each result next to what the peer-reviewed literature says about
the ground it stands on, through an extract of the CoastalWiki knowledge
base.

This manual documents all of it. Part I gets the package installed and
running. Parts II and III describe the numerical framework and the
standalone engineering formulae. Part IV is the core of the book: one
chapter per design application, each with its theory, its interface, a
worked example with the output the code actually prints, and the limits of
the method. Part V covers drawings and deliverables, Part VI the browser
app, and Part VII the test suite that keeps all of it honest. Part VIII
reproduces the complete CoastalWiki extract that ships with the app, topic
by topic, and the appendices hold the full API reference and the source of
every example.

I do not expect pyCoastal to be the tool behind groundbreaking discoveries,
although I hope it may contribute to them, or at least serve as a starting
point for someone.

Stefano Biondi
