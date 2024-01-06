\documentclass{article}

@@ if extra_packages @@
\usepackage{amsmath}
@@ endif @@

@@ if show_meta @@
\title{@= title =@}
\author{@= author =@}
\date{\today}
@@ endif @@

\begin{document}
@@ if show_meta @@
\maketitle
@@ endif @@

@@ if content @@
@= content =@
@@ endif @@

@@ block content @@
@@ endblock @@

\end{document}