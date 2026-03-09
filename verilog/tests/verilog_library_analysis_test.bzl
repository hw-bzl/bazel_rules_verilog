"""Analysis tests for verilog_library."""

load("@bazel_skylib//lib:unittest.bzl", "analysistest", "asserts")
load("//verilog:defs.bzl", "VerilogInfo")

def _file_basenames(files):
    return sorted([f.basename for f in files])

def _single_src_basename(entry):
    if len(entry.srcs) != 1:
        fail("Expected exactly one src in DAG entry, got {}".format(len(entry.srcs)))
    return entry.srcs[0].basename

def _dep_names(entry):
    return sorted([dep.label.name for dep in entry.deps])

def _leaf_provider_test_impl(ctx):
    env = analysistest.begin(ctx)
    target = analysistest.target_under_test(env)
    dag = target[VerilogInfo].dag.to_list()

    asserts.equals(env, 1, len(dag))

    entry = dag[0]
    asserts.equals(env, ["leaf.sv"], _file_basenames(entry.srcs))
    asserts.equals(env, ["leaf.svh"], _file_basenames(entry.hdrs))
    asserts.equals(env, ["leaf.dat"], _file_basenames(entry.data))
    asserts.equals(env, 0, len(entry.deps))
    asserts.equals(env, "leaf", entry.label.name)

    return analysistest.end(env)

def _transitive_dag_test_impl(ctx):
    env = analysistest.begin(ctx)
    target = analysistest.target_under_test(env)
    dag = target[VerilogInfo].dag.to_list()

    asserts.equals(env, 3, len(dag))
    asserts.equals(env, ["dep_a.sv", "dep_b.sv", "top.sv"], [_single_src_basename(entry) for entry in dag])

    # dag[i].deps captures the direct dep labels for that node.
    asserts.equals(env, [], _dep_names(dag[0]))
    asserts.equals(env, ["dep_a"], _dep_names(dag[1]))
    asserts.equals(env, ["dep_b"], _dep_names(dag[2]))

    return analysistest.end(env)

def _bad_src_extension_test_impl(ctx):
    env = analysistest.begin(ctx)
    asserts.expect_failure(env, "expected .v or .sv")
    return analysistest.end(env)

leaf_provider_test = analysistest.make(_leaf_provider_test_impl)
transitive_dag_test = analysistest.make(_transitive_dag_test_impl)
bad_src_extension_test = analysistest.make(
    _bad_src_extension_test_impl,
    expect_failure = True,
)

def verilog_library_test_suite(name):
    leaf_provider_test(
        name = name + "_leaf_provider",
        target_under_test = ":leaf",
    )

    transitive_dag_test(
        name = name + "_transitive_dag",
        target_under_test = ":top",
    )

    bad_src_extension_test(
        name = name + "_bad_src_extension",
        target_under_test = ":bad_src",
    )

    native.test_suite(
        name = name,
        tests = [
            name + "_leaf_provider",
            name + "_transitive_dag",
            name + "_bad_src_extension",
        ],
    )
