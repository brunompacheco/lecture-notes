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

Random.seed!(42)


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

set_optimizer(newsvendor, HiGHS.Optimizer)
set_silent(newsvendor)

lower_cs = Vector{Float64}()
upper_cs = Vector{Float64}()

N = [5, 10, 100, 1000, 10000]
for n in N
    set_optimizer_attribute(newsvendor, NumSamples(), n)

    optimize!(newsvendor, D)

    ci = objective_value(newsvendor)

    push!(lower_cs, ci.lower)
    push!(upper_cs, ci.upper)
end

println(upper_cs)
println(lower_cs)

plot(N, lower_cs, markershape=:circle, label="Lower bound")
plot!(N, upper_cs, markershape=:circle, xscale=:log10, label="Upper bound")
xlims!(1, 100000)
savefig("devoir1_ex3.png")