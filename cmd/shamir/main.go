package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "os"
    "strings"

    "github.com/krunixbase/shamir"
)

func main() {
    if len(os.Args) < 2 {
        usage()
        os.Exit(1)
    }

    switch os.Args[1] {
    case "split":
        runSplit(os.Args[2:])
    case "combine":
        runCombine(os.Args[2:])
    default:
        usage()
        os.Exit(1)
    }
}

func usage() {
    fmt.Fprintln(os.Stderr, "Usage:")
    fmt.Fprintln(os.Stderr, "  shamir split   -k <threshold> -n <shares> < secret")
    fmt.Fprintln(os.Stderr, "  shamir combine < shares > secret")
}

func runSplit(args []string) {
    fs := flag.NewFlagSet("split", flag.ExitOnError)
    k := fs.Int("k", 0, "threshold")
    n := fs.Int("n", 0, "number of shares")
    fs.Parse(args)

    if *k <= 0 || *n <= 0 {
        fmt.Fprintln(os.Stderr, "invalid parameters")
        os.Exit(1)
    }

    secret, err := io.ReadAll(os.Stdin)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    shares, err := shamir.Split(secret, *k, *n, os.Stdin)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    for _, s := range shares {
        text, err := shamir.MarshalText(s)
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }
        fmt.Println(text)
    }
}

func runCombine(args []string) {
    if len(args) != 0 {
        fmt.Fprintln(os.Stderr, "combine takes no flags")
        os.Exit(1)
    }

    var shares []shamir.Share
    scanner := bufio.NewScanner(os.Stdin)

    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }

        s, err := shamir.UnmarshalText(line)
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }
        shares = append(shares, s)
    }

    if err := scanner.Err(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    secret, err := shamir.Combine(shares)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    if _, err := os.Stdout.Write(secret); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
