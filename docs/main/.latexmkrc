my $rc = '../common/latexmkrc.pl';
unless (do $rc) { die "Failed to load $rc: " . ($@ || $! || 'returned false') . "\n" }
