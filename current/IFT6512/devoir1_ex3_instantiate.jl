import Pkg
Pkg.add("HiGHS")
Pkg.add("StochasticPrograms")
Pkg.add("Distributions")
Pkg.add("Plots")

using HiGHS
using StochasticPrograms
using Distributions
using Random
using Plots


@stochastic_model newsvendor begin
    @stage 1 begin
        @decision(newsvendor, x >= 0)
        @objective(newsvendor, Min, 0.15 * x)
    end
    @stage 2 begin
        @uncertain ω
        @recourse(newsvendor, y >= 0)
        @recourse(newsvendor, w >= 0)
        @objective(newsvendor, Min, - 0.25*y - 0.02*w)
        @constraint(newsvendor, y <= ω)
        @constraint(newsvendor, y + w <= x)
    end
end

@sampler Sampler = begin
    N::MvNormal

    Sampler(μ, σ) = new(MvNormal(μ, σ))

    @sample Scenario begin
        x = rand(sampler.N)
        return Scenario(ω = x[1])
    end
end

D = Sampler([650], [80])

objs = Vector{Float64}()
xs = Vector{Float64}()
ys = Vector{Float64}()
ωs = Vector{Float64}()

N = [5, 10, 100, 1000, 10000]
N = [5, 10]
for n in N
    Random.seed!(33)
    instances = instantiate(newsvendor, D, n, optimizer=HiGHS.Optimizer)

    set_silent(instances)
    optimize!(instances)

    println(n)
    push!(objs, objective_value(instances))
    push!(xs, value(all_decision_variables(instances)[1][1]))
    # push!(ys, value(all_decision_variables(instances)[2][1]))
    # push!(ωs, value(all_decision_variables(instances)[2][2]))
end

println(objs)

# plot(N, objs, xscale=:log10, markershape=:circle)
plot(N, xs, xscale=:log10, markershape=:circle, title=raw"$x^{\star}$", xlabel="Number of samples")
# plot!(N, ys, xscale=:log10, markershape=:circle, label="y")
# plot!(N, ωs, xscale=:log10, markershape=:circle, label="ω")
xlims!(1, 100000)
savefig("devoir1_ex3_xs.png")
